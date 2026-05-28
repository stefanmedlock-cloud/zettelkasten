import asyncio
import pickle
import logging

logger = logging.getLogger("ZettelkastenReplication")

class ReplicationMaster:
    def __init__(self, db):
        self.db = db
        self.replicas = set()
        self.tx_log = []

    def log_write(self, cmd, key, val, ttl=None):
        entry = {"cmd": cmd, "key": key, "val": val, "ttl": ttl}
        self.tx_log.append(entry)
        for queue in self.replicas:
            queue.put_nowait(entry)

    async def handle_replica(self, reader, writer):
        queue = asyncio.Queue()
        for entry in self.tx_log:
            queue.put_nowait(entry)
        self.replicas.add(queue)
        try:
            while True:
                entry = await queue.get()
                writer.write(pickle.dumps(entry) + b"\n\n---END---\n\n")
                await writer.drain()
        except asyncio.CancelledError:
            pass
        finally:
            self.replicas.remove(queue)
            writer.close()
            await writer.wait_closed()

class ReplicationReplica:
    def __init__(self, db, master_host, master_port):
        self.db = db
        self.master_host = master_host
        self.master_port = master_port

    async def start(self):
        while True:
            try:
                reader, writer = await asyncio.open_connection(self.master_host, self.master_port)
                buffer = b""
                while True:
                    data = await reader.read(4096)
                    if not data:
                        break
                    buffer += data
                    while b"\n\n---END---\n\n" in buffer:
                        part, buffer = buffer.split(b"\n\n---END---\n\n", 1)
                        if part:
                            entry = pickle.loads(part)
                            cmd = entry.get("cmd")
                            key = entry.get("key")
                            val = entry.get("val")
                            ttl = entry.get("ttl")
                            if cmd == "set":
                                self.db.set(key, val, ttl=ttl)
                            elif cmd == "delete":
                                self.db.delete(key)
            except Exception as e:
                logger.error(f"Replikations-Fehler: {e}. Verbinde neu...")
                await asyncio.sleep(5)
