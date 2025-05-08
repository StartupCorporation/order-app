from dw_shared_kernel import InfrastructureException


class NotAllProductDetailsWereReturned(InfrastructureException):

    def __init__(
        self,
        detail="Not all product names were returned.",
    ):
        super().__init__(detail=detail)
