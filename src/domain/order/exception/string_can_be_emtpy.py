from dw_shared_kernel import DomainException


class StringCantBeEmpty(DomainException):
    def __init__(
        self,
        detail: str = "String value can't be empty.",
    ):
        super().__init__(detail=detail)
