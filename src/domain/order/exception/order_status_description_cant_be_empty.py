from dw_shared_kernel import DomainException


class OrderStatusDescriptionCantBeEmpty(DomainException):
    def __init__(
        self,
        detail: str = "Order status description can't be empty.",
    ):
        super().__init__(detail=detail)
