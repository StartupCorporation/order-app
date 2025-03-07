from dw_shared_kernel import DomainException


class OrderedProductCantContainZeroOrLessUnits(DomainException):
    def __init__(
        self,
        detail: str = "Ordered product can't contain zero or less units.",
    ):
        super().__init__(detail=detail)
