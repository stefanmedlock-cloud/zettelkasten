import sqlite3
import time
import pickle
from typing import Any, Optional, List
from threading import RLock
from .base import BaseBackend

class SQLiteBackend(BaseBackend):
    def __init__(self, filepath: str):
        self.filepath = filepath
        self._lock = RLock()  # Lock sichert exklusiven Schreib/Lese-Verbindungsaufbau
        with self._lock:
            conn = self._get_conn()
            conn.execute(
                "CREATE TABLE IF NOT EXISTS store (key TEXT PRIMARY KEY, value BLOB, expire_at REAL)"
            )
            conn.commit()

    def _get_conn(self):
        return sqlite3.connect(self.filepath, check_same_thread=False)

    def set(self, key: str, value: Any, expire_at: Optional[float] = None) -> None:
        with self._lock:
            conn = self._get_conn()
            serialized = pickle.dumps(value)
            conn.execute(
                "INSERT OR REPLACE INTO store (key, value, expire_at) VALUES (?, ?, ?)",
                (key, serialized, expire_at)
            )
            conn.commit()

    def get(self, key: str) -> Any:
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("SELECT value, expire_at FROM store WHERE key = ?", (key,))
            row = cursor.fetchone()
            if not row:
                return None
            value_blob, expire_at = row
            if expire_at and time.time() > expire_at:
                self.delete(key)
                return None
            return pickle.loads(value_blob)

    def delete(self, key: str) -> bool:
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("DELETE FROM store WHERE key = ?", (key,))
            conn.commit()
            return cursor.rowcount > 0

    def keys(self) -> List[str]:
        with self._lock:
            conn = self._get_conn()
            cursor = conn.execute("SELECT key, expire_at FROM store")
            now = time.time()
            res = []
            for key, expire_at in cursor.fetchall():
                if expire_at and now > expire_at:
                    self.delete(key)
                else:
                    res.append(key)
            return res
