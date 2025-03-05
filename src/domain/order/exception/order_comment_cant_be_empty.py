from dw_shared_kernel import DomainException


class OrderCommentCantBeEmtpy(DomainException):
    def __init__(
        self,
        detail: str = "Order comment cant be empty.",
    ):
        super().__init__(detail)
