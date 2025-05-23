from dw_shared_kernel import CommandHandler

from application.commands.ask_for_callback_request.command import AskForCallbackRequestCommand
from domain.service.entity.callback_request import CallbackRequest
from domain.service.repository.callback_request import CallbackRequestRepository
from domain.service.service.mail import ServiceMailService
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


class AskForCallbackRequestCommandHandler(CommandHandler[AskForCallbackRequestCommand]):
    def __init__(
        self,
        callback_request_repository: CallbackRequestRepository,
        service_mail_service: ServiceMailService,
    ):
        self._callback_request_repository = callback_request_repository
        self._service_mail_service = service_mail_service

    async def __call__(
        self,
        command: AskForCallbackRequestCommand,
    ) -> None:
        callback_request = CallbackRequest.new(
            customer_personal_info=CustomerPersonalInformation.new(
                name=command.customer_personal_information.name,
                email=command.customer_personal_information.email,
                phone_number=command.customer_personal_information.phone_number,
            ),
            message_customer=command.message_customer,
            customer_note=command.customer_note,
        )

        await self._callback_request_repository.save(entity=callback_request)

        await self._service_mail_service.send_new_callback_request_asked_mail(callback_request=callback_request)
