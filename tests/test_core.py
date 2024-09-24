import pytest
from zettelkasten import Zettelkasten

def test_basic_ops():
    db = Zettelkasten()
    db.set("hallo", "welt")
    assert db.get("hallo") == "welt"
    assert db.get("nicht_existent") is None
    assert db.delete("hallo") is True
    assert db.get("hallo") is None


def test_temporary_persistence(tmp_path):
    path = str(tmp_path / 'temp.json')
    db = Zettelkasten(path)
    db.set('temp', 999)
    assert os.path.exists(path)
