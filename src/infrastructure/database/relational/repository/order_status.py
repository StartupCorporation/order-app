from domain.order.entity.order_status import OrderStatus
from domain.order.repository.order_status import OrderStatusRepository
from infrastructure.database.relational.mapper.order_status import OrderStatusEntityMapper
from infrastructure.database.relational.repository.base import AbstractSQLRepository
from infrastructure.database.relational.repository.mixin import DomainModelRepositoryMixin
from infrastructure.database.relational.tables.order_status import ORDER_STATUS_TABLE, OrderStatusTableColumn


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
        columns_to_select_string = self._get_select_columns_string(
            *OrderStatusTableColumn.get_all_columns_with_table(),
        )

        order_status_code_col = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.CODE)

        async with self._connection_manager.connect() as cur:
            record = await cur.fetchrow(
                f"""
                SELECT {columns_to_select_string}
                FROM {ORDER_STATUS_TABLE}
                WHERE {order_status_code_col} = $1
                """,
                code,
            )

        if not record:
            return

        order_status_entity = self._order_status_mapper.to_domain_model(data=record)

        return order_status_entity
