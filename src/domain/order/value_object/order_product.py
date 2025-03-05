from dataclasses import dataclass
from uuid import UUID

from dw_shared_kernel import ValueObject


@dataclass(kw_only=True, slots=True)
class OrderedProduct(ValueObject):
    product_id: UUID
    quantity: int

    @classmethod
    def new(
        cls,
        product_id: UUID,
        quantity: int,
    ) -> "OrderedProduct": ...

    @staticmethod
    def _check_quantity(quantity: int) -> None: ...
