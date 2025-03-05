from datetime import datetime
from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.database.relational.models.base import Base
from infrastructure.database.relational.models.mixins.id import IDMixin


class Comment(Base, IDMixin):
    __tablename__ = 'comment'

    author: Mapped[str] = mapped_column()
    content: Mapped[str] = mapped_column()
    created_at:  Mapped[datetime] = mapped_column()
    product_id: Mapped[UUID] = mapped_column()
