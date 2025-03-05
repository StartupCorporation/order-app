from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import UUID4, Field

from interface.web.contracts import OutputContract


class CommentOutputContract(OutputContract):
    id_: Annotated[
        UUID4,
        Field(
            examples=[uuid4()],
            alias="id",
            description="The comment's id.",
        ),
    ]
    author: Annotated[
        str,
        Field(
            examples=["John"],
            description="Person who has written the comment.",
        ),
    ]
    content: Annotated[
        str,
        Field(
            examples=["I like this!"],
            description="The comment's content.",
        ),
    ]
    created_at: Annotated[
        datetime,
        Field(
            examples=[datetime.now()],
            description="When the comment was written.",
        ),
    ]
