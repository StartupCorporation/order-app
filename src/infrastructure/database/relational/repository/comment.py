from functools import cached_property
from uuid import UUID

from sqlalchemy import delete, select

from infrastructure.database.relational.repository.base import CRUDSQLAlchemyRepository
from infrastructure.database.relational.models.comment import Comment as CommentTable
from domain.comment.entity import Comment
from domain.comment.repository import CommentRepository


class SQLAlchemyCommentRepository(
    CRUDSQLAlchemyRepository[UUID, Comment],
    CommentRepository,
):
    async def get_comments_by_product_id(
        self,
        product_id: UUID,
    ) -> list[Comment]:
        stmt = select(self.entity_class).where(self.entity_class.product_id == product_id)  # type: ignore
        return await self._scalars(stmt)

    async def delete_comments_by_product_ids(
        self,
        product_ids: list[UUID],
    ) -> None:
        stmt = delete(self.entity_class).where(CommentTable.product_id.in_(product_ids))
        return await self._execute(stmt)

    @cached_property
    def entity_class(self) -> type[Comment]:
        return Comment
