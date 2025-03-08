from enum import StrEnum, auto


ORDER_STATUS_TABLE = "order_status"


class OrderTableColumn(StrEnum):
    ID = auto()
    CODE = auto()
    NAME = auto()
    DESCRIPTION = auto()
