from dw_shared_kernel import DomainException


class ClientEmailIsInvalid(DomainException):
    def __init__(
        self,
        detail: str = "Provided client's email is not valid.",
    ):
        super().__init__(detail)
