from enum import StrEnum, auto


ORDER_TABLE = "order_"


class OrderTableColumn(StrEnum):
    ID = auto()
    COMMENT = auto()
    MESSAGE_CUSTOMER = auto()
    CREATED_AT = auto()
    CUSTOMER_INFO = auto()
    PRODUCTS = auto()
    ORDER_STATUS_ID = auto()

    @classmethod
    def get_column_with_table(
        cls,
        column: "OrderTableColumn",
    ) -> str:
        return f"{ORDER_TABLE}.{column}"

    @classmethod
    def get_all_columns_with_table(cls) -> tuple[str, ...]:
        return tuple(cls.get_column_with_table(column=column) for column in cls)
