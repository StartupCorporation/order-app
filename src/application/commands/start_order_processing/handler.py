from dw_shared_kernel import CommandHandler

from application.commands.start_order_processing.command import StartOrderProcessingCommand
from domain.order.repository.order import OrderRepository
from domain.order.service.mail import OrderMailService
from domain.order.service.order import OrderService


class StartOrderProcessingCommandHandler(CommandHandler[StartOrderProcessingCommand]):
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
        command: StartOrderProcessingCommand,
    ) -> None:
        order = await self._order_repository.get_by_id(id_=command.order_id)

        if not order:
            return

        await self._order_service.start_order_processing(order=order)

        await self._order_mail_service.send_order_processing_mail(order=order)
