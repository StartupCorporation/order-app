from uuid import uuid4

import pytest

from domain.order.exception.order_product_cant_contain_zero_or_less_units import (
    OrderedProductCantContainZeroOrLessUnits,
)
from domain.order.value_object.ordered_product import OrderedProduct


def test_ordered_product_can_be_created_with_positive_quantity() -> None:
    OrderedProduct.new(
        product_id=uuid4(),
        quantity=2,
    )


@pytest.mark.parametrize(
    "quantity",
    [-1, 0, -2],
)
def test_ordered_product_cant_be_created_with_quantity_less_or_equal_0(
    quantity: int,
) -> None:
    with pytest.raises(OrderedProductCantContainZeroOrLessUnits):
        OrderedProduct.new(
            product_id=uuid4(),
            quantity=quantity,
        )
