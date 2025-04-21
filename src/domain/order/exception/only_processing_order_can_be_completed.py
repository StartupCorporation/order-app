from dw_shared_kernel import DomainException


class OnlyProcessingOrderCanBeCompleted(DomainException):
    def __init__(
        self,
        detail: str = "Only processing order can be completed.",
    ):
        super().__init__(detail=detail)
