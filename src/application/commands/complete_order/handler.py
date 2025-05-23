from dw_shared_kernel import CommandHandler

from application.commands.complete_order.command import CompleteOrderCommand
from domain.order.repository.order import OrderRepository
from domain.order.service.mail import OrderMailService
from domain.order.service.order import OrderService


class CompleteOrderCommandHandler(CommandHandler[CompleteOrderCommand]):
    def __init__(
        self,
        order_repository: OrderRepository,
        order_service: OrderService,
        order_mail_service: OrderMailService,
    ):
        self._order_repository = order_repository
        self._order_service = order_service
        self._order_mail_service = order_mail_service

    async def __call__(
        self,
        command: CompleteOrderCommand,
    ) -> None:
        order = await self._order_repository.get_by_id(id_=command.order_id)

        if not order:
            return

        await self._order_service.complete_order(order=order)

        await self._order_mail_service.send_order_completed_mail(order=order)
