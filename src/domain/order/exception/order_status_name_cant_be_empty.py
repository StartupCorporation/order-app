from dw_shared_kernel import DomainException


class OrderStatusNameCantBeEmpty(DomainException):
    def __init__(
        self,
        detail: str = "Order status name can't be empty.",
    ):
        super().__init__(detail=detail)
