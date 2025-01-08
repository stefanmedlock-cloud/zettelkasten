import pytest
import os
import time
from zettelkasten import Zettelkasten

def test_basic_ops():
    db = Zettelkasten()
    db.set("hallo", "welt")
    assert db.get("hallo") == "welt"

def test_persistence(tmp_path):
    db_file = tmp_path / "test.json"
    db = Zettelkasten(str(db_file))
    db.set("persistenz_key", "persistenz_wert")
    
    db2 = Zettelkasten(str(db_file))
    assert db2.get("persistenz_key") == "persistenz_wert"

def test_ttl():
    db = Zettelkasten()
    db.set("kurzlebig", "daten", ttl=1)
    assert db.get("kurzlebig") == "daten"
    time.sleep(1.1)
    assert db.get("kurzlebig") is None
