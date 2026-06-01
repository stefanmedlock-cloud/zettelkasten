import pytest
import asyncio
import socket
import time
import threading
from zettelkasten.server import ZettelkastenServer
from zettelkasten import Zettelkasten

def run_server_in_thread(server):
    loop = asyncio.new_event_loop()
    def target():
        asyncio.set_event_loop(loop)
        loop.run_until_complete(server.start())
    t = threading.Thread(target=target, daemon=True)
    t.start()
    return loop, t

def test_replication():
    # Finde freie Ports
    s1 = socket.socket()
    s1.bind(('127.0.0.1', 0))
    port = s1.getsockname()[1]
    s1.close()

    master = ZettelkastenServer("127.0.0.1", port, role="master")
    master_loop, master_thread = run_server_in_thread(master)
    time.sleep(0.5)

    replica = ZettelkastenServer("127.0.0.1", port + 10, role="replica", master_addr=f"127.0.0.1:{port+1000}")
    replica_loop, replica_thread = run_server_in_thread(replica)
    time.sleep(0.5)

    db_master = Zettelkasten(f"network:127.0.0.1:{port}", backend="network")
    db_replica = Zettelkasten(f"network:127.0.0.1:{port+10}", backend="network")

    db_master.set("repl_key", "erfolg")
    time.sleep(0.8)
    
    assert db_replica.get("repl_key") == "erfolg"

    # Stop loops
    master_loop.call_soon_threadsafe(master_loop.stop)
    replica_loop.call_soon_threadsafe(replica_loop.stop)

