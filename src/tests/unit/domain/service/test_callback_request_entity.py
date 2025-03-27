from datetime import datetime

from domain.service.entity.callback_request import CallbackRequest
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


def test_callback_request_is_created(
    customer_personal_info_value_object: CustomerPersonalInformation,
) -> None:
    CallbackRequest.new(
        customer_note="some note",
        customer_personal_info=customer_personal_info_value_object,
        message_customer=True,
    )


def test_callback_request_is_created_without_customer_note(
    customer_personal_info_value_object: CustomerPersonalInformation,
) -> None:
    entity = CallbackRequest.new(
        customer_note=None,
        customer_personal_info=customer_personal_info_value_object,
        message_customer=True,
    )

    assert isinstance(entity.time_info.created_at, datetime)
