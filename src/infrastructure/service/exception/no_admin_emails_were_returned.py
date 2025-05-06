from dw_shared_kernel import InfrastructureException


class NoAdminEmailsWereReturned(InfrastructureException):

    def __init__(
        self,
        detail = "No admin emails were returned.",
    ):
        super().__init__(detail=detail)
