from dw_shared_kernel import DomainException


class StringValueTooBig(DomainException):
    def __init__(
        self,
        detail: str = "Provided string value is too big.",
    ):
        super().__init__(detail=detail)
