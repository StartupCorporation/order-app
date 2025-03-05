from dw_shared_kernel import DomainException


class OnlyNewOrderCanBeMarkedAsProcessing(DomainException):
    def __init__(
        self,
        detail: str = "Only a new order can be marked as processing.",
    ):
        super().__init__(detail)
