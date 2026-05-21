import socket
import pickle
from typing import Any, List, Optional

class ZettelkastenClient:
    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port

    def _send(self, request: dict) -> dict:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((self.host, self.port))
            s.sendall(pickle.dumps(request))
            data = s.recv(4096)
            return pickle.loads(data)

    def set(self, key: str, value: Any, ttl: Optional[int] = None):
        return self._send({"cmd": "set", "key": key, "val": value, "ttl": ttl})

    def get(self, key: str, default: Any = None) -> Any:
        res = self._send({"cmd": "get", "key": key})
        return res.get("val") if res.get("val") is not None else default

    def delete(self, key: str) -> bool:
        res = self._send({"cmd": "delete", "key": key})
        return res.get("deleted", False)

    def keys(self) -> List[str]:
        res = self._send({"cmd": "keys"})
        return res.get("keys", [])
