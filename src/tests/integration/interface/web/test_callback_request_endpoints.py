import pytest
from dw_shared_kernel import Container
from httpx import AsyncClient

from domain.service.repository.callback_request import CallbackRequestRepository


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "customer_note",
    [
        "some note",
        None,
    ],
)
async def test_ask_for_callback_request_endpoint_works_correctly_without_mocks(
    customer_note: str,
    api_client: AsyncClient,
    di_container: Container,
    clean_db: None,  # noqa: ARG001
) -> None:
    repository = di_container[CallbackRequestRepository]

    callback_requests = await repository.get_all()
    assert not callback_requests

    request_data = {
        "messageCustomer": True,
        "customerNote": customer_note,
        "personalInformation": {
            "name": "John",
            "email": "email@email.com",
            "phoneNumber": "+380664887607",
        },
    }
    response = await api_client.post(
        url="/callback_request/",
        json=request_data,
    )

    assert response.status_code == 201
    assert response.json() is None

    callback_requests = await repository.get_all()

    assert len(callback_requests) == 1
    assert (
        callback_requests[0].customer_note.content == request_data["customerNote"]  # type: ignore
        if customer_note
        else callback_requests[0].customer_note is None
    )
    assert callback_requests[0].message_customer == request_data["messageCustomer"]
    assert callback_requests[0].customer_personal_info.name == request_data["personalInformation"]["name"]
    assert callback_requests[0].customer_personal_info.email == request_data["personalInformation"]["email"]
    assert (
        callback_requests[0].customer_personal_info.phone_number == request_data["personalInformation"]["phoneNumber"]
    )
