from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager


class DatabaseTransactionManager(ABC):
    @abstractmethod
    @asynccontextmanager  # type: ignore
    async def begin(self) -> AsyncIterator[None]: ...
