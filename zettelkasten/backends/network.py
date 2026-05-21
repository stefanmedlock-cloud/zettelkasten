from .base import BaseBackend
from ..client import ZettelkastenClient
from typing import Any, Optional, List

class NetworkBackend(BaseBackend):
    def __init__(self, address: str):
        host, port_str = address.split(":")
        self.client = ZettelkastenClient(host, int(port_str))

    def set(self, key: str, value: Any, expire_at: Optional[float] = None) -> None:
        self.client.set(key, value)

    def get(self, key: str) -> Any:
        return self.client.get(key)

    def delete(self, key: str) -> bool:
        return self.client.delete(key)

    def keys(self) -> List[str]:
        return self.client.keys()
