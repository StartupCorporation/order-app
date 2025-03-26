from typing import Any
import json
from uuid import UUID

from asyncpg import Record

from domain.order.entity.order import Order
from domain.order.entity.order_status import OrderStatus
from domain.order.value_object.order_product import OrderedProduct
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from domain.service.value_object.note import Note
from domain.service.value_object.time_info import TimeInfo
from infrastructure.database.relational.mapper.base import DomainModelTableMapper


class OrderEntityMapper(DomainModelTableMapper[Order, Record]):
    def from_domain_model(
        self,
        model: Order,
    ) -> dict[str, Any]:
        values = {}

        values["id"] = model.id
        values["comment"] = model.customer_note.content if model.customer_note else None
        values["message_customer"] = model.message_customer
        values["created_at"] = model.time_info.created_at
        values["order_status_id"] = model.status.id
        values["customer_info"] = json.dumps(
            {
                "name": model.customer_personal_info.name,
                "email": model.customer_personal_info.email,
                "phone_number": model.customer_personal_info.phone_number,
            },
        )
        values["products"] = json.dumps(
            [
                {
                    "product_id": str(product.product_id),
                    "quantity": product.quantity,
                }
                for product in model.ordered_products
            ],
        )

        return values

    def to_domain_model(
        self,
        data: Record,
    ) -> Order:
        order_customer_info_data = json.loads(data["order_.customer_info"])
        order_products_data = json.loads(data["order_.products"])

        order_entity = Order(
            id=data["order_.id"],
            customer_note=None if data["order_.comment"] is None else Note(content=data["order_.comment"]),
            message_customer=data["order_.message_customer"],
            time_info=TimeInfo(created_at=data["order_.created_at"]),
            customer_personal_info=CustomerPersonalInformation(
                name=order_customer_info_data["name"],
                email=order_customer_info_data["email"],
                phone_number=order_customer_info_data["phone_number"],
            ),
            ordered_products=[
                OrderedProduct(
                    product_id=UUID(product["product_id"]),
                    quantity=product["quantity"],
                )
                for product in order_products_data
            ],
            status=OrderStatus(
                id=data["order_.order_status_id"],
                code=data["order_status.code"],
                name=data["order_status.name"],
                description=data["order_status.description"],
            ),
        )

        return order_entity
