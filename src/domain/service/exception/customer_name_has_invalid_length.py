from dw_shared_kernel import DomainException


class CustomerNameHasInvalidLength(DomainException):
    def __init__(
        self,
        detail: str = "Customer name has invalid length.",
    ):
        super().__init__(detail=detail)
