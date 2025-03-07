from domain.order.repository.order import OrderRepository
from dw_shared_kernel import CommandHandler

from domain.order.service.order import OrderService
from application.commands.start_order_processing.command import StartOrderProcessingCommand


class StartOrderProcessingCommandHandler(CommandHandler[StartOrderProcessingCommand]):
    def __init__(
        self,
        order_repository: OrderRepository,
        order_service: OrderService,
    ):
        self._order_repository = order_repository
        self._order_service = order_service

    async def __call__(
        self,
        command: StartOrderProcessingCommand,
    ) -> None:
        order = await self._order_repository.get_by_id(id_=command.order_id)

        if not order:
            return

        await self._order_service.start_order_processing(order=order)
