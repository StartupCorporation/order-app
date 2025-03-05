from dw_shared_kernel import DomainException


class InvalidOrderStatus(DomainException):
    def __init__(
        self,
        detail: str = "Specified status is invalid for the order.",
    ):
        super().__init__(detail)
