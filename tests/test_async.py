import pytest
import asyncio
from zettelkasten import AsyncZettelkasten

@pytest.mark.asyncio
async def test_async_ops(tmp_path):
    db_file = tmp_path / "async_test.json"
    db = AsyncZettelkasten(str(db_file))
    
    await db.set("key1", "wert1")
    assert await db.get("key1") == "wert1"
    
    await db.set("key2", "wert2", ttl=1)
    assert await db.get("key2") == "wert2"
    await asyncio.sleep(1.2)
    assert await db.get("key2") is None
