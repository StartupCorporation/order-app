from typing import Literal

from pydantic import BaseModel, UUID4

from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from interface.queue.contracts import MessageBrokerEvent


type FailedToReserveOrderProductsEventInputContract = MessageBrokerEvent[
    Literal["ORDER_PRODUCTS_FAILED_TO_RESERVE"],
    FailedToReserveOrderProducts,
]


class FailedToReserveOrderProducts(BaseModel):
    order_id: UUID4

    def to_command(self) -> MarkOrderAsFailedForProductsReservationCommand:
        return MarkOrderAsFailedForProductsReservationCommand(
            order_id=self.order_id,
        )
