from dw_shared_kernel import InfrastructureException


class FailedToFetchAdminEmails(InfrastructureException):

    def __init__(
        self,
        detail: str = "Failed to fetch admin emails from iac service.",
    ):
        super().__init__(detail=detail)
