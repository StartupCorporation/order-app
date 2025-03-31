from typing import Literal

from pydantic import UUID4, BaseModel

from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from interface.queue.contracts import MessageBrokerEvent


type FailedToReserveOrderProductsEventInputContract = MessageBrokerEvent[
    Literal["FAILED_TO_RESERVE_PRODUCTS"],
    FailedToReserveOrderProducts,
]


class FailedToReserveOrderProducts(BaseModel):
    order_id: UUID4

    def to_command(self) -> MarkOrderAsFailedForProductsReservationCommand:
        return MarkOrderAsFailedForProductsReservationCommand(
            order_id=self.order_id,
        )
