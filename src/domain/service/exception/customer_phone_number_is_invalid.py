from dw_shared_kernel import DomainException


class CustomerPhoneNumberIsInvalid(DomainException):
    def __init__(
        self,
        detail: str = "Provided customer's phone number is not valid.",
    ):
        super().__init__(detail=detail)
