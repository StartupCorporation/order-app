from abc import ABC
from contextlib import asynccontextmanager


class DatabaseTransactionManager(ABC):
    @asynccontextmanager  # type: ignore
    async def begin(self) -> None: ...
