from enum import StrEnum, auto


ORDER_TO_ORDER_STATUS_TABLE = "order_order_status"


class OrderTableColumn(StrEnum):
    ID = auto()
    ORDER_ID = auto()
    ORDER_STATUS_ID = auto()
