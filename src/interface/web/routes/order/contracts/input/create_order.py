from typing import Annotated
from uuid import uuid4
from pydantic import UUID4, Field

from application.commands.create_order.command import CreateOrderCommand, CustomerPersonalInfoInput, ProductInput
from interface.web.contracts import InputContract


class CreateOrderInputContract(InputContract):
    message_customer: Annotated[
        bool,
        Field(
            examples=[True],
            description="Whether the administrator has to write to the customer or no.",
        ),
    ]
    customer_comment: Annotated[
        str,
        Field(
            examples=["Text me in Telegram, please."],
            description="The customer's comment for the order.",
        ),
    ]
    products: Annotated[
        list["OrderedProductInputContract"],
        Field(
            description="List of ordered products.",
        ),
    ]
    personal_information: Annotated[
        "CustomerPersonalInformationInputContract",
        Field(
            description="Customer's personal information.",
        ),
    ]

    def to_command(self) -> CreateOrderCommand:
        return CreateOrderCommand(
            message_customer=self.message_customer,
            customer_comment=self.customer_comment,
            ordered_products=[
                ProductInput(
                    quantity=product.quantity,
                    product_id=product.product_id,
                )
                for product in self.products
            ],
            customer_personal_information=CustomerPersonalInfoInput(
                name=self.personal_information.name,
                email=self.personal_information.email,
                phone_number=self.personal_information.phone_number,
            ),
        )


class OrderedProductInputContract(InputContract):
    product_id: Annotated[
        UUID4,
        Field(
            examples=[uuid4()],
            description="The product's id.",
        ),
    ]
    quantity: Annotated[
        int,
        Field(
            examples=[3],
            description="The ordered product units amount.",
        ),
    ]


class CustomerPersonalInformationInputContract(InputContract):
    name: Annotated[
        str,
        Field(
            examples=["John"],
            description="Customer's name",
        ),
    ]
    email: Annotated[
        str,
        Field(
            examples=["customer@email.com"],
            description="Customer's email.",
        ),
    ]
    phone_number: Annotated[
        str,
        Field(
            examples=["+380961234567"],
            description="Customer's phone number",
        ),
    ]
