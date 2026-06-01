try:
    from django.core.cache.backends.base import BaseCache
except ImportError:
    class BaseCache:
        def __init__(self, *args, **kwargs): pass
        def make_key(self, key, version=None): return key

# Beispiel-Nutzung:
# CACHES = { 'default': { 'BACKEND': 'zettelkasten.contrib.django.ZettelkastenCache', 'LOCATION': 'speicher.json' } }
class ZettelkastenCache(BaseCache):
    def __init__(self, server, params):
        super().__init__(params)
        from zettelkasten.core import Zettelkasten
        self._db = Zettelkasten(server, backend=params.get("OPTIONS", {}).get("BACKEND", "json"))

    def add(self, key, value, timeout=None, version=None):
        k = self.make_key(key, version=version)
        if self._db.get(k) is not None:
            return False
        self._db.set(k, value, ttl=timeout)
        return True

    def get(self, key, default=None, version=None):
        k = self.make_key(key, version=version)
        return self._db.get(k, default=default)

    def set(self, key, value, timeout=None, version=None):
        k = self.make_key(key, version=version)
        self._db.set(k, value, ttl=timeout)

    def delete(self, key, version=None):
        k = self.make_key(key, version=version)
        return self._db.delete(k)

    def clear(self):
        for k in self._db.keys():
            self._db.delete(k)
