from dw_shared_kernel import InfrastructureException


class InvalidEmailsResponseBody(InfrastructureException):

    def __init__(
        self,
        detail: str = "IAC service returned invalid response body.",
    ):
        super().__init__(detail=detail)
