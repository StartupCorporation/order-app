from typing import Annotated

from faststream import Context
from faststream.rabbit import RabbitRouter, RabbitQueue
from dw_shared_kernel import (
    CommandBus,
    Container,
)

from interface.queue.config import config
from interface.queue.routes.order.contracts.order_products_are_reserved import (
    OrderProductsAreReservedEventInputContract,
)
from interface.queue.routes.order.contracts.failed_to_reserve_order_products import (
    FailedToReserveOrderProductsEventInputContract,
)


router = RabbitRouter()


@router.subscriber(
    queue=RabbitQueue(
        name=config.QUEUE,
        passive=True,
    ),
    description="Handles events for the orders.",
)
async def handle_product_event(
    event: OrderProductsAreReservedEventInputContract | FailedToReserveOrderProductsEventInputContract,
    container: Annotated[Container, Context()],
) -> None:
    await container[CommandBus].handle(event.data.to_command())
