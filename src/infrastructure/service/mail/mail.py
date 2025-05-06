import asyncio

from jinja2 import Environment, PackageLoader, select_autoescape

from domain.order.entity.order import Order
from domain.order.service.mail import OrderMailService
from domain.service.entity.callback_request import CallbackRequest
from domain.service.service.mail import ServiceMailService
from infrastructure.clients.catalog.client import CatalogClient
from infrastructure.clients.catalog.contracts import GetProductDetailsContract
from infrastructure.clients.iac.client import IACClient
from infrastructure.clients.iac.contracts import GetAdminsEmailContract
from infrastructure.clients.smtp import SMTPClient
from infrastructure.service.exception.no_admin_emails_were_returned import NoAdminEmailsWereReturned
from infrastructure.service.exception.not_all_product_names_were_returned import NotAllProductDetailsWereReturned
from infrastructure.service.mail.models import ProductDetailsModel


class SMTPMailService(OrderMailService, ServiceMailService):

    def __init__(
        self,
        smtp_client: SMTPClient,
        iac_client: IACClient,
        catalog_client: CatalogClient,
    ) -> None:
        self._smtp_client = smtp_client
        self._iac_client = iac_client
        self._catalog_client = catalog_client
        self._template_loader = Environment(
            loader=PackageLoader(
                package_name="infrastructure.service",
                package_path="../templates",
            ),
            autoescape=select_autoescape(),
        )

    async def send_order_created_mail(
        self,
        order: Order,
    ) -> None:
        ordered_product_details = await self._get_ordered_product_details(order=order)

        customer_template = self._template_loader.get_template("new_order_customer.html")

        await self._smtp_client.send_html(
            receivers=[order.customer_personal_info.email],
            template=customer_template.render(
                order=order,
                ordered_products=ordered_product_details,
                total_price=sum(product.price * product.quantity for product in ordered_product_details),
            ),
        )

    async def send_order_processing_mail(
        self,
        order: Order,
    ) -> None:
        ordered_product_details: list[GetProductDetailsContract]
        admins_email: GetAdminsEmailContract

        admins_email, ordered_product_details = await asyncio.gather(
            self._get_admins_email(),
            self._get_ordered_product_details(order=order),
        )

        admin_template = self._template_loader.get_template("in_progress_order_admin.html")
        customer_template = self._template_loader.get_template("in_progress_order_customer.html")

        await asyncio.gather(
            self._smtp_client.send_html(
                receivers=admins_email.emails,
                template=admin_template.render(
                    order=order,
                    ordered_products=ordered_product_details,
                    total_price=sum(product.price * product.quantity for product in ordered_product_details),
                ),
            ),
            self._smtp_client.send_html(
                receivers=[order.customer_personal_info.email],
                template=customer_template.render(
                    order=order,
                    ordered_products=ordered_product_details,
                    total_price=sum(product.price * product.quantity for product in ordered_product_details),
                ),
            ),
        )

    async def send_order_failed_to_reserve_products_mail(
        self,
        order: Order,
    ) -> None:
        ordered_product_details: list[GetProductDetailsContract]
        admins_email: GetAdminsEmailContract

        admins_email, ordered_product_details = await asyncio.gather(
            self._get_admins_email(),
            self._get_ordered_product_details(order=order),
        )

        customer_admin_template = self._template_loader.get_template("failed_order_customer_admin.html")

        await asyncio.gather(
            self._smtp_client.send_html(
                receivers=admins_email.emails,
                template=customer_admin_template.render(
                    order=order,
                    ordered_products=ordered_product_details,
                    total_price=sum(product.price * product.quantity for product in ordered_product_details),
                ),
            ),
            self._smtp_client.send_html(
                receivers=[order.customer_personal_info.email],
                template=customer_admin_template.render(
                    order=order,
                    ordered_products=ordered_product_details,
                    total_price=sum(product.price * product.quantity for product in ordered_product_details),
                ),
            ),
        )

    async def send_order_completed_mail(
        self,
        order: Order,
    ) -> None:
        ordered_product_details = await self._get_ordered_product_details(order=order)

        customer_template = self._template_loader.get_template("completed_order_customer.html")

        await self._smtp_client.send_html(
            receivers=[order.customer_personal_info.email],
            template=customer_template.render(
                order=order,
                ordered_products=ordered_product_details,
                total_price=sum(product.price * product.quantity for product in ordered_product_details),
            ),
        )

    async def send_new_callback_request_asked_mail(
        self,
        callback_request: CallbackRequest,
    ) -> None:
        admins_email = await self._iac_client.get_admins_email()

        admin_template = self._template_loader.get_template("new_callback_request_admin.html")

        await self._smtp_client.send_html(
            receivers=admins_email.emails,
            template=admin_template.render(callback_request=callback_request),
        )

    async def _get_ordered_product_details(
        self,
        order: Order,
    ) -> tuple[ProductDetailsModel, ...]:
        ordered_product_ids = {
            product.product_id: product
            for product in order.ordered_products
        }

        products = await self._catalog_client.get_product_details(
            ids=ordered_product_ids.keys(),
        )

        returned_products = tuple(product.id for product in products)

        if any(filter(lambda product_id: product_id not in returned_products, ordered_product_ids)):
            raise NotAllProductDetailsWereReturned()

        return tuple(
            ProductDetailsModel(
                name=product.name,
                price=product.price,
                quantity=ordered_product_ids[product.id].quantity,
            )
            for product in products
        )

    async def _get_admins_email(self) -> GetAdminsEmailContract:
        response = await self._iac_client.get_admins_email()

        if not response.emails:
            raise NoAdminEmailsWereReturned()

        return response
