import asyncio
import pickle
import logging
from .core import Zettelkasten
from .replication import ReplicationMaster, ReplicationReplica

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ZettelkastenServer")

class ZettelkastenServer:
    def __init__(self, host: str, port: int, db_path: str = None, backend: str = "json", role: str = None, master_addr: str = None):
        self.host = host
        self.port = port
        self.db = Zettelkasten(db_path, backend=backend)
        self.role = role
        self.master_addr = master_addr
        self.master_manager = ReplicationMaster(self.db) if role == "master" else None

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        try:
            while True:
                data = await reader.read(4096)
                if not data:
                    break
                request = pickle.loads(data)
                cmd = request.get("cmd")
                key = request.get("key")
                val = request.get("val")
                ttl = request.get("ttl")

                response = {"status": "ok"}
                if cmd == "set":
                    self.db.set(key, val, ttl=ttl)
                    if self.master_manager:
                        self.master_manager.log_write("set", key, val, ttl)
                elif cmd == "get":
                    response["val"] = self.db.get(key)
                elif cmd == "delete":
                    response["deleted"] = self.db.delete(key)
                    if self.master_manager:
                        self.master_manager.log_write("delete", key, None)
                elif cmd == "keys":
                    response["keys"] = self.db.keys()
                else:
                    response = {"status": "error", "message": "Unbekannter Befehl"}

                writer.write(pickle.dumps(response))
                await writer.drain()
        except Exception as e:
            logger.error(f"Fehler bei Verbindung mit {addr}: {e}")
        finally:
            writer.close()
            await writer.wait_closed()

    async def start(self):
        tasks = []
        if self.role == "master":
            # Start replica-handshake server
            replication_server = await asyncio.start_server(
                self.master_manager.handle_replica, self.host, self.port + 1000
            )
            logger.info(f"Replikations-Master gestartet unter {self.host}:{self.port + 1000}")
            tasks.append(replication_server.serve_forever())
        elif self.role == "replica" and self.master_addr:
            m_host, m_port_str = self.master_addr.split(":")
            replica_manager = ReplicationReplica(self.db, m_host, int(m_port_str))
            logger.info(f"Replica startet Verbindung mit Master {self.master_addr}")
            tasks.append(replica_manager.start())

        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logger.info(f"Client Server gestartet unter {self.host}:{self.port}")
        tasks.append(server.serve_forever())
        
        await asyncio.gather(*tasks)
