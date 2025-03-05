from dw_shared_kernel import DomainException


class OrderCantContainNoProducts(DomainException):
    def __init__(
        self,
        detail: str = "Order cant contain no products.",
    ):
        super().__init__(detail)
