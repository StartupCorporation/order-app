import json
from json import JSONDecodeError
from typing import Iterable
from uuid import UUID

from httpx import URL
from pydantic import ValidationError

from infrastructure.clients.catalog.contracts import GetProductDetailsContract
from infrastructure.clients.catalog.exception.failed_to_fetch_product_details import FailedToFetchProductDetails
from infrastructure.clients.catalog.exception.invalid_product_details_response_body import (
    InvalidProductDetailsResponseBody,
)
from infrastructure.clients.http_ import HTTPClient
from infrastructure.settings.catalog import CatalogServiceSettings


class CatalogClient:

    def __init__(
        self,
        http_client: HTTPClient,
        catalog_settings: CatalogServiceSettings,
    ):
        self._http_client = http_client
        self._catalog_settings = catalog_settings

    async def get_product_details(
        self,
        ids: Iterable[UUID],
    ) -> tuple[GetProductDetailsContract, ...]:
        body, status_code = await self._http_client.get(
            url=URL(
                host=self._catalog_settings.HOST,
                port=self._catalog_settings.PORT,
                path="/api/products/by-ids",
                params={"ids": list(ids)},
                scheme="http",
            ),
            headers={
                "API_KEY": self._catalog_settings.API_KEY,
            },
        )

        if not 200 <= status_code < 300:
            raise FailedToFetchProductDetails(
                f"Failed to fetch product names from catalog service. "
                f"Service responded with {status_code} status code and {body} body.",
            )

        try:
            return tuple(
                GetProductDetailsContract.model_validate(detail)
                for detail in json.loads(body)
            )
        except (ValidationError, JSONDecodeError):
            raise InvalidProductDetailsResponseBody()
