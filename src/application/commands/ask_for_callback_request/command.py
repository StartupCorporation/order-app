from dw_shared_kernel import Command
from pydantic import BaseModel


class AskForCallbackRequestCommand(Command):
    customer_personal_information: "CustomerPersonalInfoInput"
    customer_note: str
    message_customer: bool


class CustomerPersonalInfoInput(BaseModel):
    name: str
    email: str
    phone_number: str
