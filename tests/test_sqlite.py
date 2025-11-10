import pytest
import os
import time
from zettelkasten import Zettelkasten

def test_sqlite_backend(tmp_path):
    db_file = tmp_path / "test.db"
    db = Zettelkasten(str(db_file), backend="sqlite")
    
    db.set("key1", "wert1")
    assert db.get("key1") == "wert1"
    
    db.set("key2", "wert2", ttl=1)
    assert db.get("key2") == "wert2"
    time.sleep(1.2)
    assert db.get("key2") is None
