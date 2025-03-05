from typing import Annotated
from uuid import uuid4
from interface.web.contracts import InputContract
from pydantic import UUID4, Field


class CreateCommentInputContract(InputContract):
    product_id: Annotated[
        UUID4,
        Field(
            examples=[uuid4()],
            description="Product's id for which comment must be created.",
        ),
    ]
    author: Annotated[
        str,
        Field(
            examples=["John"],
            description="Comment authors' name.",
        ),
    ]
    content: Annotated[
        str,
        Field(
            examples=["Awesome thing!"],
            description="The comment content which is written by user.",
        ),
    ]
