import pytest

from application.commands.ask_for_callback_request.command import (
    AskForCallbackRequestCommand,
    CustomerPersonalInfoInput,
)
from application.commands.ask_for_callback_request.handler import AskForCallbackRequestCommandHandler
from domain.service.repository.callback_request import CallbackRequestRepository


@pytest.mark.asyncio
async def test_command_handler_stores_callback_request(
    callback_request_repository: CallbackRequestRepository,
) -> None:
    handler = AskForCallbackRequestCommandHandler(
        callback_request_repository=callback_request_repository,
    )
    await handler(
        command=AskForCallbackRequestCommand(
            message_customer=True,
            customer_note=None,
            customer_personal_information=CustomerPersonalInfoInput(
                name="name",
                email="email@email.com",
                phone_number="+380661234567",
            ),
        ),
    )
