import pytest

from domain.service.exception.customer_email_is_invalid import CustomerEmailIsInvalid
from domain.service.exception.customer_name_cant_be_empty import CustomerNameCantBeEmpty
from domain.service.exception.customer_name_has_invalid_length import CustomerNameHasInvalidLength
from domain.service.exception.customer_phone_number_is_invalid import CustomerPhoneNumberIsInvalid
from domain.service.value_object.customer_personal_info import CustomerPersonalInformation


def test_customer_personal_information_created() -> None:
    CustomerPersonalInformation.new(
        name="name",
        email="some@email.com",
        phone_number="+380661234567",
    )


def test_customer_personal_information_cant_be_created_with_name_greater_64_chars() -> None:
    with pytest.raises(CustomerNameHasInvalidLength):
        CustomerPersonalInformation.new(
            name="1" * 65,
            email="some@email.com",
            phone_number="+380661234567",
        )


def test_customer_personal_information_cant_be_empty() -> None:
    with pytest.raises(CustomerNameCantBeEmpty):
        CustomerPersonalInformation.new(
            name="     ",
            email="some@email.com",
            phone_number="+380661234567",
        )


@pytest.mark.parametrize(
    "phone_number",
    [
        "380661234567",
        "sss",
        "",
        "123555",
    ],
)
def test_customer_personal_information_cant_be_created_with_invalid_phone_number(
    phone_number: str,
) -> None:
    with pytest.raises(CustomerPhoneNumberIsInvalid):
        CustomerPersonalInformation.new(
            name="name",
            email="some@email.com",
            phone_number=phone_number,
        )


@pytest.mark.parametrize(
    "email",
    [
        "asfsafa",
        "soe1@e",
        "@.com",
        "123555",
    ],
)
def test_customer_personal_information_cant_be_created_with_invalid_email(
    email: str,
) -> None:
    with pytest.raises(CustomerEmailIsInvalid):
        CustomerPersonalInformation.new(
            name="name",
            email=email,
            phone_number="+380661234567",
        )
