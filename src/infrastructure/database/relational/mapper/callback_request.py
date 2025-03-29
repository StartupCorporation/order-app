import json
from typing import Any

from asyncpg import Record

from domain.service.entity.callback_request import CallbackRequest
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation
from domain.service.value_object.note import Note
from domain.service.value_object.time_info import TimeInfo
from infrastructure.database.relational.mapper.base import DomainModelTableMapper


class CallbackRequestEntityMapper(DomainModelTableMapper[CallbackRequest, Record]):
    def from_domain_model(
        self,
        model: CallbackRequest,
    ) -> dict[str, Any]:
        values = {}

        values["id"] = model.id
        values["customer_note"] = None if model.customer_note is None else model.customer_note.content
        values["message_customer"] = model.message_customer
        values["created_at"] = model.time_info.created_at
        values["customer_info"] = json.dumps(
            {
                "name": model.customer_personal_info.name,
                "email": model.customer_personal_info.email,
                "phone_number": model.customer_personal_info.phone_number,
            },
        )

        return values

    def to_domain_model(
        self,
        data: Record,
    ) -> CallbackRequest:
        callback_request_customer_info_data = json.loads(data["callback_request.customer_info"])

        callback_request_entity = CallbackRequest(
            id=data["callback_request.id"],
            customer_note=(
                None
                if not data["callback_request.customer_note"]
                else Note(content=data["callback_request.customer_note"])
            ),
            customer_personal_info=CustomerPersonalInformation(
                name=callback_request_customer_info_data["name"],
                email=callback_request_customer_info_data["email"],
                phone_number=callback_request_customer_info_data["phone_number"],
            ),
            message_customer=data["callback_request.message_customer"],
            time_info=TimeInfo(created_at=data["callback_request.created_at"]),
        )

        return callback_request_entity
