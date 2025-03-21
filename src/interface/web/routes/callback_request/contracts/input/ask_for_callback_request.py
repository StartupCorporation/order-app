from typing import Annotated
from pydantic import Field

from interface.web.contracts import InputContract
from application.commands.ask_for_callback_request.command import (
    AskForCallbackRequestCommand,
    CustomerPersonalInfoInput,
)


class AskForCallbackRequestInputContract(InputContract):
    message_customer: Annotated[
        bool,
        Field(
            examples=[True],
            description="Whether the administrator has to write to the customer or no.",
        ),
    ]
    customer_note: Annotated[
        str,
        Field(
            examples=["Text me in Telegram, please."],
            description="The customer's note for the order.",
        ),
    ]
    personal_information: Annotated[
        "CustomerPersonalInformationInputContract",
        Field(
            description="Customer's personal information.",
        ),
    ]

    def to_command(self) -> AskForCallbackRequestCommand:
        return AskForCallbackRequestCommand(
            message_customer=self.message_customer,
            customer_note=self.customer_note,
            customer_personal_information=CustomerPersonalInfoInput(
                name=self.personal_information.name,
                email=self.personal_information.email,
                phone_number=self.personal_information.phone_number,
            ),
        )


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
