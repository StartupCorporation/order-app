from collections.abc import Iterable
from email.message import EmailMessage

import aiosmtplib

from infrastructure.settings.smtp import SMTPSettings


class SMTPClient:
    def __init__(
        self,
        smtp_settings: SMTPSettings,
    ) -> None:
        self._smtp_settings = smtp_settings

    async def send_html(
        self,
        receivers: Iterable[str],
        template: str,
    ) -> None:
        message = EmailMessage()

        message["Subject"] = "Link"
        message["From"] = self._smtp_settings.SENDER_EMAIL
        message["To"] = ", ".join(receivers)
        message.set_content(
            template,
            subtype="html",
        )

        await self._send(message=message)

    async def _send(
        self,
        message: EmailMessage,
    ) -> None:
        await aiosmtplib.send(
            message,
            hostname=self._smtp_settings.HOST,
            port=self._smtp_settings.PORT,
            password=self._smtp_settings.PASSWORD,
            username=self._smtp_settings.USERNAME,
        )
