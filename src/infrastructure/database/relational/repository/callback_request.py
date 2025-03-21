import asyncpg

from domain.service.entity.callback_request import CallbackRequest
from domain.service.repository.callback_request import CallbackRequestRepository
from infrastructure.database.relational.mapper.callback_request import CallbackRequestEntityMapper
from infrastructure.database.relational.repository.base import AbstractSQLRepository
from infrastructure.database.relational.repository.mixin import DomainModelRepositoryMixin


class SQLCallbackRequestRepository(AbstractSQLRepository, DomainModelRepositoryMixin, CallbackRequestRepository):
    def __init__(
        self,
        *args,
        callback_request_entity_mapper: CallbackRequestEntityMapper,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._callback_request_entity_mapper = callback_request_entity_mapper

    async def save(
        self,
        entity: CallbackRequest,
    ) -> None:
        insert_values = self._callback_request_entity_mapper.from_domain_model(model=entity)
        update_values = {key: value for key, value in insert_values.items() if key != "id"}

        insert_placeholders = self._get_inline_placeholders_string(
            amount=len(insert_values),
            start_position=1,
        )
        update_placeholders = self._get_placeholders_tuple(
            amount=len(update_values),
            start_position=len(insert_values) + 1,
        )

        async with self._connection_manager.connect() as cur:
            try:
                await cur.execute(
                    f"""
                    INSERT INTO callback_request ({", ".join(insert_values.keys())})
                    VALUES ({insert_placeholders})
                    ON CONFLICT (id) DO UPDATE
                    SET {
                        ",\n".join(
                            f"{col} = {placeholder}"
                            for col, placeholder in zip(update_values.keys(), update_placeholders)
                        )
                    }
                    """,
                    *insert_values.values(),
                    *update_values.values(),
                )
            except asyncpg.PostgresError as e:
                raise e
