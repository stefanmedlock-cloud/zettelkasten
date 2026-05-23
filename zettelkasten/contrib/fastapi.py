from zettelkasten.core import Zettelkasten
from typing import Generator

_db_instance = None

def init_db(filepath: str = None, backend: str = "json"):
    global _db_instance
    _db_instance = Zettelkasten(filepath, backend=backend)
    return _db_instance

def get_db() -> Generator[Zettelkasten, None, None]:
    if not _db_instance:
        raise RuntimeError("Zettelkasten DB ist nicht initialisiert.")
    yield _db_instance
