import pytest
import asyncio
import socket
from zettelkasten.server import ZettelkastenServer
from zettelkasten import Zettelkasten

@pytest.mark.asyncio
async def test_replication():
    # Finde freie Ports
    s1 = socket.socket()
    s1.bind(('127.0.0.1', 0))
    port = s1.getsockname()[1]
    s1.close()

    master = ZettelkastenServer("127.0.0.1", port, role="master")
    master_task = asyncio.create_task(master.start())
    await asyncio.sleep(0.5)

    replica = ZettelkastenServer("127.0.0.1", port + 10, role="replica", master_addr=f"127.0.0.1:{port+1000}")
    replica_task = asyncio.create_task(replica.start())
    await asyncio.sleep(0.5)

    db_master = Zettelkasten(f"network:127.0.0.1:{port}", backend="network")
    db_replica = Zettelkasten(f"network:127.0.0.1:{port+10}", backend="network")

    db_master.set("repl_key", "erfolg")
    await asyncio.sleep(0.5)
    
    assert db_replica.get("repl_key") == "erfolg"

    master_task.cancel()
    replica_task.cancel()
    try:
        await asyncio.gather(master_task, replica_task)
    except asyncio.CancelledError:
        pass
