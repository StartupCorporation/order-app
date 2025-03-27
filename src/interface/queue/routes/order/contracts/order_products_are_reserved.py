from typing import Literal

from pydantic import UUID4, BaseModel

from application.commands.start_order_processing.command import StartOrderProcessingCommand
from interface.queue.contracts import MessageBrokerEvent

type OrderProductsAreReservedEventInputContract = MessageBrokerEvent[
    Literal["PRODUCTS_RESERVED_FOR_ORDER"],
    OrderProductsAreReserved,
]


class OrderProductsAreReserved(BaseModel):
    order_id: UUID4

    def to_command(self) -> StartOrderProcessingCommand:
        return StartOrderProcessingCommand(
            order_id=self.order_id,
        )
