from dw_shared_kernel import DomainException


class NoteContentIsLong(DomainException):
    def __init__(
        self,
        detail: str = "Customer order's note is too long.",
    ):
        super().__init__(detail=detail)
