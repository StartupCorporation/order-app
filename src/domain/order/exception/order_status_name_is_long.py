from dw_shared_kernel import DomainException


class OrderStatusNameIsLong(DomainException):
    def __init__(
        self,
        detail: str = "Order status name is long.",
    ):
        super().__init__(detail=detail)
