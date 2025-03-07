from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from domain.order.repository.order import OrderRepository
from domain.order.service.order import OrderService
from dw_shared_kernel import CommandHandler


class MarkOrderAsFailedForProductsReservationCommandHandler(
    CommandHandler[MarkOrderAsFailedForProductsReservationCommand],
):
    def __init__(
        self,
        order_service: OrderService,
        order_repository: OrderRepository,
    ):
        self._order_service = order_service
        self._order_repository = order_repository

    async def __call__(
        self,
        command: MarkOrderAsFailedForProductsReservationCommand,
    ) -> None:
        order = await self._order_repository.get_by_id(id_=command.order_id)

        if not order:
            return

        await self._order_service.mark_order_as_failed_for_products_reservation(order=order)
