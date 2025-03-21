from dw_shared_kernel import DomainException


class OrderStatusCodeCantBeEmpty(DomainException):
    def __init__(
        self,
        detail: str = "Order status code can't be empty.",
    ):
        super().__init__(detail=detail)
