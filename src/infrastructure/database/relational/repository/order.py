from uuid import UUID

import asyncpg

from domain.order.entity.order import Order
from domain.order.repository.order import OrderRepository
from infrastructure.database.relational.mapper.order import OrderEntityMapper
from infrastructure.database.relational.repository.base import AbstractSQLRepository
from infrastructure.database.relational.repository.mixin import DomainModelRepositoryMixin
from infrastructure.database.relational.tables.order import ORDER_TABLE, OrderTableColumn
from infrastructure.database.relational.tables.order_status import ORDER_STATUS_TABLE, OrderStatusTableColumn


class SQLOrderRepository(AbstractSQLRepository, DomainModelRepositoryMixin, OrderRepository):
    def __init__(
        self,
        *args,
        order_entity_mapper: OrderEntityMapper,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._order_entity_mapper = order_entity_mapper

    async def get_by_id(
        self,
        id_: UUID,
    ) -> Order | None:
        columns_to_select_string = self._get_select_columns_string(
            *OrderTableColumn.get_all_columns_with_table(),
            *OrderStatusTableColumn.get_all_columns_with_table(),
        )

        order_id_col = OrderTableColumn.get_column_with_table(OrderTableColumn.ID)
        order_order_status_id_col = OrderTableColumn.get_column_with_table(OrderTableColumn.ORDER_STATUS_ID)
        order_status_id_col = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.ID)

        async with self._connection_manager.connect() as cur:
            record = await cur.fetchrow(
                f"""
                SELECT {columns_to_select_string}
                FROM
                    {ORDER_TABLE} JOIN {ORDER_STATUS_TABLE} ON {order_order_status_id_col} = {order_status_id_col}
                WHERE {order_id_col} = $1
                """,
                id_,
            )

        if not record:
            return

        return self._order_entity_mapper.to_domain_model(data=record)

    async def save(
        self,
        entity: Order,
    ) -> None:
        insert_order_values = self._order_entity_mapper.from_domain_model(model=entity)
        update_order_values = self._order_entity_mapper.from_domain_model(model=entity)
        update_order_values.pop(OrderTableColumn.ID)

        insert_placeholders = self._get_inline_placeholders_string(
            amount=len(insert_order_values),
            start_position=1,
        )
        update_placeholders = self._get_placeholders_tuple(
            amount=len(update_order_values),
            start_position=len(insert_order_values) + 1,
        )

        async with self._connection_manager.connect() as cur:
            try:
                await cur.execute(
                    f"""
                    INSERT INTO {ORDER_TABLE} ({", ".join(insert_order_values.keys())})
                    VALUES ({insert_placeholders})
                    ON CONFLICT ({OrderTableColumn.ID}) DO UPDATE
                    SET {
                        ",\n".join(
                            f"{col} = {placeholder}"
                            for col, placeholder in zip(update_order_values.keys(), update_placeholders)
                        )
                    }
                    """,
                    *insert_order_values.values(),
                    *update_order_values.values(),
                )
            except asyncpg.PostgresError as e:
                raise e
