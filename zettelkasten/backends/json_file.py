import os
import json
import time
import zlib
from typing import Any, Optional, List
from threading import RLock
from .base import BaseBackend

class JSONFileBackend(BaseBackend):
    def __init__(self, filepath: str, compress: bool = False):
        self.filepath = filepath
        self.compress = compress
        self._data = {}
        self._lock = RLock()
        self._load()

    def _load(self):
        if os.path.exists(self.filepath):
            try:
                with open(self.filepath, "rb" if self.compress else "r") as f:
                    raw_data = f.read()
                    if self.compress and raw_data:
                        raw_data = zlib.decompress(raw_data).decode("utf-8")
                    if raw_data:
                        loaded = json.loads(raw_data)
                        self._data = {k: tuple(v) for k, v in loaded.items()}
            except (json.JSONDecodeError, zlib.error):
                self._data = {}

    def _save(self):
        serialized = json.dumps(self._data).encode("utf-8")
        if self.compress:
            serialized = zlib.compress(serialized)
            with open(self.filepath, "wb") as f:
                f.write(serialized)
        else:
            with open(self.filepath, "w") as f:
                f.write(serialized.decode("utf-8"))

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
