from typing import Any
from asyncpg import Record

from domain.order.entity.order_status import OrderStatus
from infrastructure.database.relational.mapper.base import DomainModelTableMapper
from infrastructure.database.relational.tables.order_status import OrderStatusTableColumn


class OrderStatusEntityMapper(DomainModelTableMapper[OrderStatus, Record, OrderStatusTableColumn]):
    def from_domain_model(
        self,
        model: OrderStatus,
    ) -> dict[OrderStatusTableColumn, Any]:
        values = {}

        values[OrderStatusTableColumn.ID] = model.id
        values[OrderStatusTableColumn.CODE] = model.code
        values[OrderStatusTableColumn.NAME] = model.name
        values[OrderStatusTableColumn.DESCRIPTION] = model.description

        return values

    def to_domain_model(
        self,
        data: Record,
    ) -> OrderStatus:
        order_status_id = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.ID)
        order_status_code = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.CODE)
        order_status_name = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.NAME)
        order_status_description = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.DESCRIPTION)

        order_status_entity = OrderStatus(
            id=data[order_status_id],
            code=data[order_status_code],
            name=data[order_status_name],
            description=data[order_status_description],
        )

        return order_status_entity
