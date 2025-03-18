from uuid import UUID

from dw_shared_kernel import Command
from pydantic import BaseModel


class CreateOrderCommand(Command):
    ordered_products: list["ProductInput"]
    customer_personal_information: "CustomerPersonalInfoInput"
    customer_comment: str
    message_customer: bool


class ProductInput(BaseModel):
    product_id: UUID
    quantity: int


class CustomerPersonalInfoInput(BaseModel):
    name: str
    email: str
    phone_number: str
