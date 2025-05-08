from dw_shared_kernel import InfrastructureException


class FailedToFetchProductDetails(InfrastructureException):

    def __init__(
        self,
        detail: str = "Failed to fetch product details from catalog service.",
    ):
        super().__init__(detail=detail)
