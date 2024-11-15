import pytest
import os
from zettelkasten import Zettelkasten

def test_basic_ops():
    db = Zettelkasten()
    db.set("hallo", "welt")
    assert db.get("hallo") == "welt"
    assert db.delete("hallo") is True

def test_persistence(tmp_path):
    db_file = tmp_path / "test.json"
    db = Zettelkasten(str(db_file))
    db.set("persistenz_key", "persistenz_wert")
    
    db2 = Zettelkasten(str(db_file))
    assert db2.get("persistenz_key") == "persistenz_wert"
