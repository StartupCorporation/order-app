from domain.order.entity.order_status import OrderStatus
from domain.order.repository.order_status import OrderStatusRepository
from infrastructure.database.relational.mapper.order_status import OrderStatusEntityMapper
from infrastructure.database.relational.repository.base import AbstractSQLRepository
from infrastructure.database.relational.repository.mixin import DomainModelRepositoryMixin


class SQLOrderStatusRepository(AbstractSQLRepository, DomainModelRepositoryMixin, OrderStatusRepository):
    def __init__(
        self,
        *args,
        order_status_mapper: OrderStatusEntityMapper,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._order_status_mapper = order_status_mapper

    async def get_by_code(
        self,
        code: str,
    ) -> OrderStatus | None:
        async with self._connection_manager.connect() as cur:
            record = await cur.fetchrow(
                """
                SELECT
                    id AS "order_status.id",
                    name AS "order_status.name",
                    code AS "order_status.code",
                    description AS "order_status.description"
                FROM
                    order_status
                WHERE
                    order_status.code = $1
                """,
                code,
            )

        if not record:
            return

        order_status_entity = self._order_status_mapper.to_domain_model(data=record)

        return order_status_entity
