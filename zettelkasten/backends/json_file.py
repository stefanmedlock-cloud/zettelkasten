import os
import json
import time
from typing import Any, Optional, List
from threading import RLock
from .base import BaseBackend

class JSONFileBackend(BaseBackend):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._data = {}
        self._lock = RLock()
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data = {k: tuple(v) for k, v in loaded.items()}
            except json.JSONDecodeError:
                self._data = {}

    def _save(self):
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def set(self, key: str, value: Any, expire_at: Optional[float] = None) -> None:
        with self._lock:
            self._data[key] = (value, expire_at)
            self._save()

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
                self._save()
                return True
            return False

    def keys(self) -> List[str]:
        with self._lock:
            current_keys = []
            for key in list(self._data.keys()):
                if self.get(key) is not None:
                    current_keys.append(key)
            return current_keys
