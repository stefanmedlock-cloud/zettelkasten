import time
from typing import Any, Optional
from .backends.memory import MemoryBackend
from .backends.json_file import JSONFileBackend

class Zettelkasten:
    def __init__(self, filepath: Optional[str] = None):
        if filepath:
            self.backend = JSONFileBackend(filepath)
        else:
            self.backend = MemoryBackend()

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

