from abc import ABC, abstractmethod

from domain.service.entity.callback_request import CallbackRequest


class ServiceMailService(ABC):
    @abstractmethod
    async def send_new_callback_request_asked_mail(self, callback_request: CallbackRequest) -> None: ...
