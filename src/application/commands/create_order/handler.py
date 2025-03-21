from dw_shared_kernel import CommandHandler

from application.commands.create_order.command import CreateOrderCommand
from domain.order.service.order import OrderService
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from domain.order.value_object.order_product import OrderedProduct


class CreateOrderCommandHandler(CommandHandler[CreateOrderCommand]):
    def __init__(
        self,
        order_service: OrderService,
    ):
        self._order_service = order_service

    async def __call__(
        self,
        command: CreateOrderCommand,
    ) -> None:
        await self._order_service.create_new_order(
            message_customer=command.message_customer,
            customer_note=command.customer_note,
            customer_personal_information=CustomerPersonalInformation.new(
                name=command.customer_personal_information.name,
                email=command.customer_personal_information.email,
                phone_number=command.customer_personal_information.phone_number,
            ),
            ordered_products=[
                OrderedProduct.new(product_id=product.product_id, quantity=product.quantity)
                for product in command.ordered_products
            ],
        )
