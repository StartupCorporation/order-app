from dw_shared_kernel import DomainException


class ClientPhoneNumberIsInvalid(DomainException):
    def __init__(
        self,
        detail: str = "Provided client's phonen number is not valid.",
    ):
        super().__init__(detail)
