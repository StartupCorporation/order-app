from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4

from dw_shared_kernel import Entity

from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from domain.service.value_object.note import Note
from domain.service.value_object.time_info import TimeInfo


@dataclass(kw_only=True, slots=True)
class CallbackRequest(Entity):
    __hash__ = Entity.__hash__

    customer_personal_info: CustomerPersonalInformation
    customer_note: Note | None
    message_customer: bool
    time_info: TimeInfo

    @classmethod
    def new(
        cls,
        customer_personal_info: CustomerPersonalInformation,
        customer_note: str | None,
        message_customer: bool,
    ) -> "CallbackRequest":
        return CallbackRequest(
            id=uuid4(),
            customer_personal_info=customer_personal_info,
            message_customer=message_customer,
            customer_note=Note.new(content=customer_note) if customer_note else None,
            time_info=TimeInfo.new(
                created_at=datetime.now(),
            ),
        )
