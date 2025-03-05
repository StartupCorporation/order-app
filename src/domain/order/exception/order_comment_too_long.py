from dw_shared_kernel import DomainException


class OrderCommentTooLong(DomainException):
    def __init__(
        self,
        detail: str = "Order comment too long.",
    ):
        super().__init__(detail)
