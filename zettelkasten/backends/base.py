from abc import ABC, abstractmethod
from typing import Any, Optional, List

class BaseBackend(ABC):
    @abstractmethod
    def set(self, key: str, value: Any, expire_at: Optional[float] = None) -> None:
        pass

    @abstractmethod
    def get(self, key: str) -> Any:
        pass

    @abstractmethod
    def delete(self, key: str) -> bool:
        pass

    @abstractmethod
    def keys(self) -> List[str]:
        pass
