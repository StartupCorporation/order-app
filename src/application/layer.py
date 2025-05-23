from dw_shared_kernel import CommandBus, Container, Layer

from application.commands.ask_for_callback_request.command import AskForCallbackRequestCommand
from application.commands.ask_for_callback_request.handler import AskForCallbackRequestCommandHandler
from application.commands.complete_order.command import CompleteOrderCommand
from application.commands.complete_order.handler import CompleteOrderCommandHandler
from application.commands.create_order.command import CreateOrderCommand
from application.commands.create_order.handler import CreateOrderCommandHandler
from application.commands.mark_order_as_failed_for_products_reservation.command import (
    MarkOrderAsFailedForProductsReservationCommand,
)
from application.commands.mark_order_as_failed_for_products_reservation.handler import (
    MarkOrderAsFailedForProductsReservationCommandHandler,
)
from application.commands.start_order_processing.command import StartOrderProcessingCommand
from application.commands.start_order_processing.handler import StartOrderProcessingCommandHandler
from domain.order.repository.order import OrderRepository
from domain.order.service.mail import OrderMailService
from domain.order.service.order import OrderService
from domain.service.repository.callback_request import CallbackRequestRepository
from domain.service.service.mail import ServiceMailService


class ApplicationLayer(Layer):
    def setup(self, container: Container) -> None:
        container[CommandBus].register(
            command=CreateOrderCommand,
            handler=CreateOrderCommandHandler(
                order_service=container[OrderService],
                order_mail_service=container[OrderMailService],
            ),
        )
        container[CommandBus].register(
            command=MarkOrderAsFailedForProductsReservationCommand,
            handler=MarkOrderAsFailedForProductsReservationCommandHandler(
                order_service=container[OrderService],
                order_repository=container[OrderRepository],
                order_mail_service=container[OrderMailService],
            ),
        )
        container[CommandBus].register(
            command=StartOrderProcessingCommand,
            handler=StartOrderProcessingCommandHandler(
                order_repository=container[OrderRepository],
                order_service=container[OrderService],
                order_mail_service=container[OrderMailService],
            ),
        )
        container[CommandBus].register(
            command=CompleteOrderCommand,
            handler=CompleteOrderCommandHandler(
                order_repository=container[OrderRepository],
                order_service=container[OrderService],
                order_mail_service=container[OrderMailService],
            ),
        )
        container[CommandBus].register(
            command=AskForCallbackRequestCommand,
            handler=AskForCallbackRequestCommandHandler(
                callback_request_repository=container[CallbackRequestRepository],
                service_mail_service=container[ServiceMailService],
            ),
        )
