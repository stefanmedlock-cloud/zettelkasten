import time
from typing import Any, Optional
from .backends.memory import MemoryBackend
from .backends.json_file import JSONFileBackend
from .backends.sqlite import SQLiteBackend
from .backends.network import NetworkBackend

class Zettelkasten:
    def __init__(self, filepath: Optional[str] = None, backend: str = "json", compress: bool = False):
        if backend == "network" or (filepath and filepath.startswith("network:")):
            addr = filepath.split("network:")[1] if filepath and filepath.startswith("network:") else filepath
            self.backend = NetworkBackend(addr or "localhost:8080")
        elif not filepath:
            self.backend = MemoryBackend()
        elif backend == "sqlite" or filepath.endswith(".db") or filepath.endswith(".sqlite"):
            self.backend = SQLiteBackend(filepath)
        else:
            self.backend = JSONFileBackend(filepath, compress=compress)

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        expire_at = time.time() + ttl if ttl else None
        self.backend.set(key, value, expire_at)

    def get(self, key: str, default: Any = None) -> Any:
        val = self.backend.get(key)
        return val if val is not None else default

    def delete(self, key: str) -> bool:
        return self.backend.delete(key)

    def keys(self):
        return self.backend.keys()
