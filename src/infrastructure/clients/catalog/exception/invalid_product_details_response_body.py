from dw_shared_kernel import InfrastructureException


class InvalidProductDetailsResponseBody(InfrastructureException):

    def __init__(
        self,
        detail: str = "Catalog service returned invalid response body for product details.",
    ):
        super().__init__(detail=detail)
