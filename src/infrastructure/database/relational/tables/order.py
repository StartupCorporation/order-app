from enum import StrEnum, auto


ORDER_TABLE = "order"


class OrderTableColumn(StrEnum):
    ID = auto()
    COMMENT = auto()
    MESSAGE_CUSTOMER = auto()
    CREATED_AT = auto()
    CUSTOMER_INFO = auto()
    PRODUCTS = auto()
