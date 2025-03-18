from abc import ABC

from infrastructure.database.relational.connection import SQLConnectionManager


class AbstractSQLRepository(ABC):
    def __init__(
        self,
        connection_manager: SQLConnectionManager,
    ):
        self._connection_manager = connection_manager
