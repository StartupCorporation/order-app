from dataclasses import dataclass
from enum import auto
from typing import cast
from uuid import uuid4

from dw_shared_kernel import (
    Entity,
    ValueNameEnum,
)

from domain.order.exception.new_order_status_code_duplicates_builtin_codes import (
    NewOrderStatusCodeDuplicatesBuiltInCode,
)
from domain.order.exception.string_can_be_emtpy import StringCantBeEmpty
from domain.order.exception.string_value_too_big import StringValueTooBig


@dataclass(kw_only=True)
class OrderStatus(Entity):
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
        cls._check_new_code_isnt_builtin(code=code)
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
        if len(code) > 128:
            raise StringValueTooBig("Order status's code too big.")

    @staticmethod
    def _check_new_code_isnt_builtin(code: str) -> None:
        if code in BuiltInOrderStatus:
            raise NewOrderStatusCodeDuplicatesBuiltInCode()

    @staticmethod
    def _check_name(name: str) -> None:
        if len(name) >= 128:
            raise StringValueTooBig("Order status's name too big.")

    @staticmethod
    def _check_description(description: str | None) -> None:
        if not (description is None or description.strip()):
            raise StringCantBeEmpty("Order status's description can't be empty string.")

        if len(cast(str, description)) > 512:
            raise StringValueTooBig("Order status's description too big.")

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
