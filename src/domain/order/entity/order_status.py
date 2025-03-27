from dataclasses import dataclass
from enum import auto
from uuid import uuid4

from dw_shared_kernel import (
    Entity,
    NotEmptyStringSpecification,
    StringLengthSpecification,
    ValueNameEnum,
)

from domain.order.exception.new_order_status_code_duplicates_builtin_codes import (
    NewOrderStatusCodeDuplicatesBuiltInCode,
)
from domain.order.exception.order_status_code_cant_be_empty import OrderStatusCodeCantBeEmpty
from domain.order.exception.order_status_code_is_long import OrderStatusCodeIsLong
from domain.order.exception.order_status_description_cant_be_empty import OrderStatusDescriptionCantBeEmpty
from domain.order.exception.order_status_description_is_long import OrderStatusDescriptionIsLong
from domain.order.exception.order_status_name_cant_be_empty import OrderStatusNameCantBeEmpty
from domain.order.exception.order_status_name_is_long import OrderStatusNameIsLong


@dataclass(kw_only=True, slots=True)
class OrderStatus(Entity):
    __hash__ = Entity.__hash__

    code: str
    name: str
    description: str | None

    @classmethod
    def new(
        cls,
        code: str,
        name: str,
        description: str | None,
    ) -> "OrderStatus":
        cls._check_code(code=code)
        cls._check_description(description=description)
        cls._check_name(name=name)

        return cls(
            id=uuid4(),
            code=code,
            name=name,
            description=description,
        )

    @staticmethod
    def _check_code(code: str) -> None:
        if not NotEmptyStringSpecification(can_be_nullable=False).is_satisfied_by(value=code):
            raise OrderStatusCodeCantBeEmpty()

        if not StringLengthSpecification(min_length=1, max_length=128).is_satisfied_by(value=code):
            raise OrderStatusCodeIsLong("Order status's code too big.")

        if code in BuiltInOrderStatus:
            raise NewOrderStatusCodeDuplicatesBuiltInCode()

    @staticmethod
    def _check_name(name: str) -> None:
        if not NotEmptyStringSpecification(can_be_nullable=False).is_satisfied_by(value=name):
            raise OrderStatusNameCantBeEmpty()

        if not StringLengthSpecification(min_length=1, max_length=128).is_satisfied_by(value=name):
            raise OrderStatusNameIsLong("Order status's name too big.")

    @staticmethod
    def _check_description(description: str | None) -> None:
        if not NotEmptyStringSpecification(can_be_nullable=True).is_satisfied_by(value=description):
            raise OrderStatusDescriptionCantBeEmpty()

        if description and not StringLengthSpecification(
            min_length=1,
            max_length=512,
        ).is_satisfied_by(
            value=description,
        ):
            raise OrderStatusDescriptionIsLong()

    @property
    def is_new(self) -> bool:
        return self.code == BuiltInOrderStatus.NEW.name

    @property
    def is_processing(self) -> bool:
        return self.code == BuiltInOrderStatus.PROCESSING.name

    @property
    def is_products_reservation_failed(self) -> bool:
        return self.code == BuiltInOrderStatus.PRODUCTS_RESERVATION_FAILED.name


class BuiltInOrderStatus(ValueNameEnum):
    NEW = auto()
    PROCESSING = auto()
    PRODUCTS_RESERVATION_FAILED = auto()
    COMPLETED = auto()
    FAILED = auto()
