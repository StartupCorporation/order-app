from typing import Annotated

from fastapi import APIRouter, Body, status, Depends
from dw_shared_kernel import (
    Container,
    CommandBus,
)

from interface.web.dependencies.container import get_di_container
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
