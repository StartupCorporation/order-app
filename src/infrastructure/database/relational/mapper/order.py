from typing import Any
import json
from uuid import UUID

from asyncpg import Record

from domain.order.entity.order import Order
from domain.order.entity.order_status import OrderStatus
from domain.order.value_object.customer_personal_info import CustomerPersonalInformation
from domain.order.value_object.order_product import OrderedProduct
from infrastructure.database.relational.mapper.base import DomainModelTableMapper
from infrastructure.database.relational.tables.order import OrderTableColumn
from infrastructure.database.relational.tables.order_status import OrderStatusTableColumn


class OrderEntityMapper(DomainModelTableMapper[Order, Record, OrderTableColumn]):
    def from_domain_model(
        self,
        model: Order,
    ) -> dict[OrderTableColumn, Any]:
        values = {}

        values[OrderTableColumn.ID] = model.id
        values[OrderTableColumn.COMMENT] = model.customer_comment
        values[OrderTableColumn.MESSAGE_CUSTOMER] = model.message_customer
        values[OrderTableColumn.CREATED_AT] = model.created_at
        values[OrderTableColumn.ORDER_STATUS_ID] = model.status.id
        values[OrderTableColumn.CUSTOMER_INFO] = json.dumps(
            {
                "name": model.customer_personal_info.name,
                "email": model.customer_personal_info.email,
                "phone_number": model.customer_personal_info.phone_number,
            },
        )
        values[OrderTableColumn.PRODUCTS] = json.dumps(
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
        order_id = OrderTableColumn.get_column_with_table(OrderTableColumn.ID)
        order_comment = OrderTableColumn.get_column_with_table(OrderTableColumn.COMMENT)
        order_message_customer = OrderTableColumn.get_column_with_table(OrderTableColumn.MESSAGE_CUSTOMER)
        order_created_at = OrderTableColumn.get_column_with_table(OrderTableColumn.CREATED_AT)
        order_customer_info = OrderTableColumn.get_column_with_table(OrderTableColumn.CUSTOMER_INFO)
        order_products = OrderTableColumn.get_column_with_table(OrderTableColumn.PRODUCTS)
        order_order_status_id = OrderTableColumn.get_column_with_table(OrderTableColumn.ORDER_STATUS_ID)

        order_status_code = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.CODE)
        order_status_name = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.NAME)
        order_status_description = OrderStatusTableColumn.get_column_with_table(OrderStatusTableColumn.DESCRIPTION)

        order_customer_info_data = json.loads(data[order_customer_info])
        order_products_data = json.loads(data[order_products])

        order_entity = Order(
            id=data[order_id],
            customer_comment=data[order_comment],
            message_customer=data[order_message_customer],
            created_at=data[order_created_at],
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
                id=data[order_order_status_id],
                code=data[order_status_code],
                name=data[order_status_name],
                description=data[order_status_description],
            ),
        )

        return order_entity
