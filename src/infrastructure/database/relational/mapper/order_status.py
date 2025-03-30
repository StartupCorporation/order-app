from typing import Any

from asyncpg import Record

from domain.order.entity.order_status import OrderStatus
from infrastructure.database.relational.mapper.base import DomainModelTableMapper


class OrderStatusEntityMapper(DomainModelTableMapper[OrderStatus, Record]):
    def from_domain_model(
        self,
        model: OrderStatus,
    ) -> dict[str, Any]:
        values = {}

        values["id"] = model.id
        values["code"] = model.code
        values["name"] = model.name
        values["description"] = model.description

        return values

    def to_domain_model(
        self,
        data: Record,
    ) -> OrderStatus:
        order_status_entity = OrderStatus(
            id=data["order_status.id"],
            code=data["order_status.code"],
            name=data["order_status.name"],
            description=data["order_status.description"],
        )

        return order_status_entity
