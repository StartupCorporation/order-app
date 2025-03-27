from dataclasses import dataclass
from uuid import UUID

from dw_shared_kernel import ValueObject

from domain.order.exception.order_product_cant_contain_zero_or_less_units import (
    OrderedProductCantContainZeroOrLessUnits,
)


@dataclass(kw_only=True, slots=True)
class OrderedProduct(ValueObject):
    product_id: UUID
    quantity: int

    @classmethod
    def new(
        cls,
        product_id: UUID,
        quantity: int,
    ) -> "OrderedProduct":
        cls._check_quantity(quantity=quantity)

        return cls(
            product_id=product_id,
            quantity=quantity,
        )

    @staticmethod
    def _check_quantity(quantity: int) -> None:
        if quantity <= 0:
            raise OrderedProductCantContainZeroOrLessUnits()
