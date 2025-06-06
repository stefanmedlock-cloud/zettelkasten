import asyncio
from typing import Any, Optional, List
from .core import Zettelkasten

class AsyncZettelkasten:
    def __init__(self, filepath: str = None):
        self._db = Zettelkasten(filepath)
        self._loop = asyncio.get_event_loop()

    async def set(self, key: str, value: Any, ttl: Optional[int] = None):
        return await self._loop.run_in_executor(None, self._db.set, key, value, ttl)

    async def get(self, key: str, default: Any = None) -> Any:
        return await self._loop.run_in_executor(None, self._db.get, key, default)

    async def delete(self, key: str) -> bool:
        return await self._loop.run_in_executor(None, self._db.delete, key)

    async def keys(self) -> List[str]:
        return await self._loop.run_in_executor(None, self._db.keys)
