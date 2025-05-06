from httpx import URL
from pydantic import ValidationError

from infrastructure.clients.http_ import HTTPClient
from infrastructure.clients.iac.contracts import GetAdminsEmailContract
from infrastructure.clients.iac.exception.failed_to_fetch_admin_emails import FailedToFetchAdminEmails
from infrastructure.clients.iac.exception.invalid_emails_response_body import InvalidEmailsResponseBody
from infrastructure.settings.iac import IACSettings


class IACClient:

    def __init__(
        self,
        http_client: HTTPClient,
        iac_settings: IACSettings,
    ):
        self._http_client = http_client
        self._iac_settings = iac_settings

    async def get_admins_email(self) -> GetAdminsEmailContract:
        body, status_code = await self._http_client.get(
            url=URL(
                host=self._iac_settings.HOST,
                port=self._iac_settings.PORT,
                path="/api/identities",
                scheme='http',
            ),
            headers={
                "X-Api-Key": self._iac_settings.API_KEY,
            },
        )

        if not 200 <= status_code < 300:
            raise FailedToFetchAdminEmails(
                f"Failed to fetch admin emails from iac service. "
                f"Service responded with {status_code} status code and {body} body.",
            )

        try:
            return GetAdminsEmailContract.model_validate_json(body)
        except ValidationError:
            raise InvalidEmailsResponseBody()
