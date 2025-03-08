from abc import ABC
from enum import StrEnum

from infrastructure.database.relational.connection import SQLConnectionManager


class AbstractSQLRepository(ABC):
    def __init__(
        self,
        table_name: str,
        columns: StrEnum,
        connection_manager: SQLConnectionManager,
    ):
        self._table = table_name
        self._columns = columns
        self._connection_manager = connection_manager
