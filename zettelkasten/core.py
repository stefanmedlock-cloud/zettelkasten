import json
import os
import time
from threading import RLock

class Zettelkasten:
    def __init__(self, filepath: str = None):
        self._data = {}
        self.filepath = filepath
        self._lock = RLock()
        if filepath and os.path.exists(filepath):
            self.load()

    def set(self, key: str, value, ttl: int = None):
        with self._lock:
            expire_at = time.time() + ttl if ttl else None
            self._data[key] = (value, expire_at)
            if self.filepath:
                self.save()

    def get(self, key: str, default=None):
        with self._lock:
            if key not in self._data:
                return default
            value, expire_at = self._data[key]
            if expire_at and time.time() > expire_at:
                self.delete(key)
                return default
            return value

    def delete(self, key: str) -> bool:
        with self._lock:
            if key in self._data:
                del self._data[key]
                if self.filepath:
                    self.save()
                return True
            return False

    def keys(self):
        with self._lock:
            current_keys = []
            for key in list(self._data.keys()):
                if self.get(key) is not None:
                    current_keys.append(key)
            return current_keys

    def save(self):
        with self._lock:
            if not self.filepath:
                return
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(self._data, f)

    def load(self):
        with self._lock:
            if not self.filepath or not os.path.exists(self.filepath):
                return
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    loaded = json.load(f)
                    self._data = {k: tuple(v) for k, v in loaded.items()}
            except json.JSONDecodeError:
                self._data = {}
