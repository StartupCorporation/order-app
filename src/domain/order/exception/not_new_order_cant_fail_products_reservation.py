from dw_shared_kernel import DomainException


class NotNewOrderCantFailProductsReservation(DomainException):
    def __init__(
        self,
        detail: str = "Not new order can't fail products reservation.",
    ):
        super().__init__(detail=detail)
