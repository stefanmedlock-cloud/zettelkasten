import asyncio
import pickle
import logging
from .core import Zettelkasten

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ZettelkastenServer")

class ZettelkastenServer:
    def __init__(self, host: str, port: int, db_path: str = None, backend: str = "json"):
        self.host = host
        self.port = port
        self.db = Zettelkasten(db_path, backend=backend)

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
                elif cmd == "get":
                    response["val"] = self.db.get(key)
                elif cmd == "delete":
                    response["deleted"] = self.db.delete(key)
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
        server = await asyncio.start_server(self.handle_client, self.host, self.port)
        logger.info(f"Server gestartet unter {self.host}:{self.port}")
        async with server:
            await server.serve_forever()
