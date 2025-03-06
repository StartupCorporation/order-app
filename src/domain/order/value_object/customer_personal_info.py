from dataclasses import dataclass

from email_validator import EmailNotValidError, validate_email
import phonenumbers

from domain.order.exception.customer_phone_number_is_invalid import CustomerPhoneNumberIsInvalid
from domain.order.exception.customer_email_is_invalid import CustomerEmailIsInvalid
from domain.order.exception.string_can_be_emtpy import StringCantBeEmpty
from domain.order.exception.string_value_too_big import StringValueTooBig
from dw_shared_kernel import ValueObject


@dataclass(kw_only=True, slots=True)
class CustomerPersonalInformation(ValueObject):
    name: str
    email: str
    phone_number: str

    @classmethod
    def new(
        cls,
        name: str,
        email: str,
        phone_number: str,
    ) -> "CustomerPersonalInformation":
        cls._check_name(name=name)
        cls._check_phone_number(phone_number=phone_number)

        return cls(
            name=name,
            email=cls._normalize_email(email=email),
            phone_number=phone_number,
        )

    @staticmethod
    def _check_name(name: str) -> None:
        if not (name is None or name.strip()):
            raise StringCantBeEmpty("Customer's name can't be empty.")

        if len(name) > 64:
            raise StringValueTooBig("Customer's name too big.")

    @staticmethod
    def _normalize_email(email: str) -> str:
        try:
            validated_email = validate_email(email)
        except EmailNotValidError:
            raise CustomerEmailIsInvalid()

        return validated_email.normalized

    @staticmethod
    def _check_phone_number(phone_number: str) -> None:
        if not phonenumbers.is_possible_number(phonenumbers.parse(phone_number)):
            raise CustomerPhoneNumberIsInvalid()
