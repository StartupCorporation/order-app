from dw_shared_kernel import DomainException


class NewOrderStatusCodeDuplicatesBuiltInCode(DomainException):
    def __init__(
        self,
        detail: str = "New order status's code duplicates built-in codes.",
    ):
        super().__init__(detail=detail)
