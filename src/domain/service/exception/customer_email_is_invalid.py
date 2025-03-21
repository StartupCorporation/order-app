from dw_shared_kernel import DomainException


class CustomerEmailIsInvalid(DomainException):
    def __init__(
        self,
        detail: str = "Provided customer's email is not valid.",
    ):
        super().__init__(detail=detail)
