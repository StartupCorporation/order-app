from typing import Annotated

from fastapi import APIRouter, Body, status, Depends
from dw_shared_kernel import (
    Container,
    CommandBus,
)

from interface.web.dependencies.container import get_di_container
from interface.web.routes.callback_request.contracts.input.ask_for_callback_request import (
    AskForCallbackRequestInputContract,
)


router = APIRouter(
    prefix="/callback_request",
    tags=["Callback Request"],
)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
)
async def ask_for_callback_request(
    callback_request_data: Annotated[
        AskForCallbackRequestInputContract,
        Body(description="The data for creating a new callback request."),
    ],
    container: Annotated[Container, Depends(get_di_container)],
) -> None:
    """
    Create a new callback request.
    """
    await container[CommandBus].handle(
        command=callback_request_data.to_command(),
    )
