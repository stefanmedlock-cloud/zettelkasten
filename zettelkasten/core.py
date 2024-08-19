class Zettelkasten:
    """
    Hauptklasse für die Zettelkasten Key-Value-Datenbank.
    """
    def __init__(self):
        self._data = {}

    def set(self, key: str, value):
        self._data[key] = value

    def get(self, key: str, default=None):
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        if key in self._data:
            del self._data[key]
            return True
        return False

    def keys(self):
        return list(self._data.keys())
