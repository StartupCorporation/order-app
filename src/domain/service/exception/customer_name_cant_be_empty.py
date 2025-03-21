from dw_shared_kernel import DomainException


class CustomerNameCantBeEmpty(DomainException):
    def __init__(
        self,
        detail: str = "Customer name cant be empty.",
    ):
        super().__init__(detail=detail)
