from typing import Annotated

from dw_shared_kernel import (
    CommandBus,
    Container,
    get_di_container,
    verify_token,
)
from fastapi import APIRouter, Body, Depends, Path, status
from pydantic import UUID4

from application.commands.complete_order.command import CompleteOrderCommand
from interface.web.routes.order.contracts.input.create_order import CreateOrderInputContract


router = APIRouter(
    prefix="/order",
    tags=["Order"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def create_new_order(
    order_data: Annotated[CreateOrderInputContract, Body(description="The data for creating a new order.")],
    container: Annotated[Container, Depends(get_di_container)],
) -> None:
    """
    Create a new order with provided products.
    """
    await container[CommandBus].handle(
        command=order_data.to_command(),
    )


@router.post(
    "/{order_id}/complete/",
    status_code=status.HTTP_200_OK,
)
async def complete_order(
    order_id: Annotated[UUID4, Path(description="Order's `id` to complete.")],
    container: Annotated[Container, Depends(get_di_container)],
    _: Annotated[None, Depends(verify_token)],
) -> None:
    """
    Completes specified order.
    """
    await container[CommandBus].handle(
        command=CompleteOrderCommand(order_id=order_id),
    )
