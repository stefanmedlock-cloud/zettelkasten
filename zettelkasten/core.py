import json
import os

class Zettelkasten:
    def __init__(self, filepath: str = None):
        self._data = {}
        self.filepath = filepath
        if filepath and os.path.exists(filepath):
            self.load()

    def set(self, key: str, value):
        self._data[key] = value
        if self.filepath:
            self.save()

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            if self.filepath:
                self.save()
            return True
        return False

    def keys(self):
        return list(self._data.keys())

    def save(self):
        if not self.filepath:
            return
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(self._data, f)

    def load(self):
        if not self.filepath or not os.path.exists(self.filepath):
            return
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                self._data = json.load(f)
        except json.JSONDecodeError:
            self._data = {}

