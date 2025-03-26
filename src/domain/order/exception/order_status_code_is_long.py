from dw_shared_kernel import DomainException


class OrderStatusCodeIsLong(DomainException):
    def __init__(
        self,
        detail: str = "Order status code is long.",
    ):
        super().__init__(detail=detail)
