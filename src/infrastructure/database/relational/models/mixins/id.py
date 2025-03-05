from uuid import UUID, uuid4

from sqlalchemy import func
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class IDMixin:
    id: Mapped[UUID] = mapped_column(
        primary_key=True,
        name='id',
        default=uuid4,
        server_default=func.gen_random_uuid(),
    )
