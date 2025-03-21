from dw_shared_kernel import DomainException


class CustomerNameIsLong(DomainException):
    def __init__(
        self,
        detail: str = "Customer name is long.",
    ):
        super().__init__(detail=detail)
