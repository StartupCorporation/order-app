from dw_shared_kernel import DomainException


class OrderStatusNotFound(DomainException):
    def __init__(
        self,
        detail: str = "Specified order status doesn't exist.",
    ):
        super().__init__(detail=detail)
