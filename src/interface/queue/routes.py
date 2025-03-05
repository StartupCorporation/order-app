from typing import Annotated

from faststream import Context
from faststream.rabbit import RabbitRouter, RabbitQueue
from dw_shared_kernel import (
    CommandBus,
    Container,
)

from interface.queue.config import config
from interface.queue.contracts.product.product_deleted import ProductDeletedEventInputContract


router = RabbitRouter()


@router.subscriber(
    queue=RabbitQueue(
        name=config.PRODUCT_QUEUE,
        passive=True,
    ),
    description="Handles events for the products.",
)
async def handle_product_event(
    event: ProductDeletedEventInputContract,
    container: Annotated[Container, Context()],
) -> None:
    await container[CommandBus].handle(event.data.to_command())
