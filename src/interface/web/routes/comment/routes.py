from typing import Annotated

from fastapi import APIRouter, Path, Query, status, Depends
from interface.web.routes.comment.docs.create_comment import CREATE_COMMENT
from interface.web.routes.comment.docs.delete_comment import DELETE_COMMENT
from pydantic import UUID4
from dw_shared_kernel import (
    QueryBus,
    Container,
    CommandBus,
)

from interface.web.routes.comment.contracts.input.create_comment import CreateCommentInputContract
from interface.web.dependencies.container import get_di_container
from interface.web.routes.comment.contracts.output.get_categories import CommentOutputContract
from interface.web.routes.comment.docs.get_product_comments import GET_PRODUCT_COMMENTS
from application.queries.get_product_comments.query import GetProductCommentsQuery
from application.commands.create_comment.command import CreateCommentCommand
from application.commands.delete_comment.command import DeleteCommentCommand


router = APIRouter(
    prefix="/comment",
    tags=["Comment"],
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    responses=GET_PRODUCT_COMMENTS,  # type: ignore
)
async def get_product_comments(
    container: Annotated[Container, Depends(get_di_container)],
    product_id: Annotated[UUID4, Query(description="Product's `id` whose comments must be returned.")],
) -> list[CommentOutputContract]:
    """
    Returns all comments for the specified product.
    """
    return await container[QueryBus].handle(
        query=GetProductCommentsQuery(
            product_id=product_id,
        ),
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    responses=CREATE_COMMENT,  # type: ignore
)
async def create_comment(
    container: Annotated[Container, Depends(get_di_container)],
    comment: CreateCommentInputContract,
) -> None:
    """
    Creates a new comment for the specific product.
    """
    await container[CommandBus].handle(
        command=CreateCommentCommand(
            product_id=comment.product_id,
            author=comment.author,
            content=comment.content,
        ),
    )


@router.delete(
    "/{comment_id}/",
    status_code=status.HTTP_204_NO_CONTENT,
    responses=DELETE_COMMENT,  # type: ignore
)
async def delete_comment(
    container: Annotated[Container, Depends(get_di_container)],
    comment_id: Annotated[UUID4, Path(description="Comment's `id`.")],
) -> None:
    """
    Deletes a comment by its `id`.
    """
    await container[CommandBus].handle(
        command=DeleteCommentCommand(
            id=comment_id,
        ),
    )
