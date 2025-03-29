from uuid import UUID

import asyncpg

from domain.order.entity.order import Order
from domain.order.repository.order import OrderRepository
from infrastructure.database.relational.mapper.order import OrderEntityMapper
from infrastructure.database.relational.repository.base import AbstractSQLRepository
from infrastructure.database.relational.repository.mixin import DomainModelRepositoryMixin


class SQLOrderRepository(AbstractSQLRepository, DomainModelRepositoryMixin, OrderRepository):
    def __init__(
        self,
        *args,
        order_entity_mapper: OrderEntityMapper,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._order_entity_mapper = order_entity_mapper

    async def get_all(self) -> list[Order]:
        async with self._connection_manager.connect() as cur:
            records = await cur.fetch(
                """
                SELECT
                    order_.id AS "order_.id",
                    order_.comment AS "order_.comment",
                    order_.message_customer AS "order_.message_customer",
                    order_.created_at AS "order_.created_at",
                    order_.customer_info AS "order_.customer_info",
                    order_.products AS "order_.products",
                    order_.order_status_id AS "order_.order_status_id",
                    order_status.name AS "order_status.name",
                    order_status.code AS "order_status.code",
                    order_status.description AS "order_status.description"
                FROM
                    order_ JOIN order_status ON order_.order_status_id = order_status.id
                """,
            )

        return [self._order_entity_mapper.to_domain_model(data=record) for record in records]

    async def get_by_id(
        self,
        id_: UUID,
    ) -> Order | None:
        async with self._connection_manager.connect() as cur:
            record = await cur.fetchrow(
                """
                SELECT
                    order_.id AS "order_.id",
                    order_.comment AS "order_.comment",
                    order_.message_customer AS "order_.message_customer",
                    order_.created_at AS "order_.created_at",
                    order_.customer_info AS "order_.customer_info",
                    order_.products AS "order_.products",
                    order_.order_status_id AS "order_.order_status_id",
                    order_status.name AS "order_status.name",
                    order_status.code AS "order_status.code",
                    order_status.description AS "order_status.description"
                FROM
                    order_ JOIN order_status ON order_.order_status_id = order_status.id
                WHERE
                    order_.id = $1
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
        update_order_values = {key: value for key, value in insert_order_values.items() if key != "id"}

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
                    INSERT INTO order_ ({", ".join(insert_order_values.keys())})
                    VALUES ({insert_placeholders})
                    ON CONFLICT (id) DO UPDATE
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
