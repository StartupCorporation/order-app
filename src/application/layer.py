from dw_shared_kernel import CommandBus, Container, Layer

from application.commands.start_order_processing.command import StartOrderProcessingCommand
from application.commands.start_order_processing.handler import StartOrderProcessingCommandHandler
from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from application.commands.mark_order_as_failed_for_products_reservation.handler import (
    MarkOrderAsFailedForProductsReservationCommandHandler,
)
from application.commands.create_order.command import CreateOrderCommand
from application.commands.create_order.handler import CreateOrderCommandHandler
from domain.order.repository.order import OrderRepository
from domain.order.service.order import OrderService


class ApplicationLayer(Layer):
    def setup(self, container: Container) -> None:
        container[CommandBus].register(
            command=CreateOrderCommand,
            handler=CreateOrderCommandHandler(
                order_service=container[OrderService],
            ),
        )
        container[CommandBus].register(
            command=MarkOrderAsFailedForProductsReservationCommand,
            handler=MarkOrderAsFailedForProductsReservationCommandHandler(
                order_service=container[OrderService],
                order_repository=container[OrderRepository],
            ),
        )
        container[CommandBus].register(
            command=StartOrderProcessingCommand,
            handler=StartOrderProcessingCommandHandler(
                order_repository=container[OrderRepository],
                order_service=container[OrderService],
            ),
        )
