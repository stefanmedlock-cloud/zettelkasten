import time
from typing import Any, Optional, List
from threading import RLock
from .base import BaseBackend

class MemoryBackend(BaseBackend):
    def __init__(self):
        self._data = {}
        self._lock = RLock()

    def set(self, key: str, value: Any, expire_at: Optional[float] = None) -> None:
        with self._lock:
            self._data[key] = (value, expire_at)

    def get(self, key: str) -> Any:
        with self._lock:
            if key not in self._data:
                return None
            value, expire_at = self._data[key]
            if expire_at and time.time() > expire_at:
                self.delete(key)
                return None
            return value

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                return True
            return False

    def keys(self) -> List[str]:
        with self._lock:
            current_keys = []
            for key in list(self._data.keys()):
                if self.get(key) is not None:
                    current_keys.append(key)
            return current_keys
