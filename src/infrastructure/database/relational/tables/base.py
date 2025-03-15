from abc import abstractmethod
from typing import Protocol, Self


class TableColumn(Protocol):
    @abstractmethod
    @classmethod
    def get_column_with_table(cls, column: Self) -> str: ...

    @abstractmethod
    @classmethod
    def get_all_columns_with_table(cls) -> tuple[str, ...]: ...
