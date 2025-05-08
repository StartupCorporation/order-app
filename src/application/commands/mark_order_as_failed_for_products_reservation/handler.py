from dw_shared_kernel import CommandHandler

from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from domain.order.repository.order import OrderRepository
from domain.order.service.mail import OrderMailService
from domain.order.service.order import OrderService


class MarkOrderAsFailedForProductsReservationCommandHandler(
    CommandHandler[MarkOrderAsFailedForProductsReservationCommand],
):
    def __init__(
        self,
        order_service: OrderService,
        order_repository: OrderRepository,
        order_mail_service: OrderMailService,
    ):
        self._order_service = order_service
        self._order_repository = order_repository
        self._order_mail_service = order_mail_service

    async def __call__(
        self,
        command: MarkOrderAsFailedForProductsReservationCommand,
    ) -> None:
        order = await self._order_repository.get_by_id(id_=command.order_id)

        if not order:
            return

        await self._order_service.mark_order_as_failed_for_products_reservation(order=order)

        await self._order_mail_service.send_order_failed_to_reserve_products_mail(order=order)
