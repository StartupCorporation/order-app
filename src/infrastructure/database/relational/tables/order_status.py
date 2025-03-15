from enum import StrEnum, auto


ORDER_STATUS_TABLE = "order_status"


class OrderStatusTableColumn(StrEnum):
    ID = auto()
    CODE = auto()
    NAME = auto()
    DESCRIPTION = auto()

    @classmethod
    def get_column_with_table(
        cls,
        column: "OrderStatusTableColumn",
    ) -> str:
        return f"{ORDER_STATUS_TABLE}.{column}"

    @classmethod
    def get_all_columns_with_table(cls) -> tuple[str, ...]:
        return tuple(cls.get_column_with_table(column=column) for column in cls)
