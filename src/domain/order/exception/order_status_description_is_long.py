from dw_shared_kernel import DomainException


class OrderStatusDescriptionIsLong(DomainException):
    def __init__(
        self,
        detail: str = "Order is description is long.",
    ):
        super().__init__(detail=detail)
