from dataclasses import dataclass

import phonenumbers
from dw_shared_kernel import NotEmptyStringSpecification, StringLengthSpecification, ValueObject
from email_validator import EmailNotValidError, validate_email

from domain.service.exception.customer_email_is_invalid import CustomerEmailIsInvalid
from domain.service.exception.customer_name_cant_be_empty import CustomerNameCantBeEmpty
from domain.service.exception.customer_name_has_invalid_length import CustomerNameHasInvalidLength
from domain.service.exception.customer_phone_number_is_invalid import CustomerPhoneNumberIsInvalid


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
        if not NotEmptyStringSpecification(can_be_nullable=False).is_satisfied_by(value=name):
            raise CustomerNameCantBeEmpty()

        if not StringLengthSpecification(min_length=1, max_length=64).is_satisfied_by(value=name):
            raise CustomerNameHasInvalidLength("Customer name must be greater than 1 and less than 64 characters.")

    @staticmethod
    def _normalize_email(email: str) -> str:
        try:
            validated_email = validate_email(email)
        except EmailNotValidError:
            raise CustomerEmailIsInvalid()

        return validated_email.normalized

    @staticmethod
    def _check_phone_number(phone_number: str) -> None:
        try:
            if not phonenumbers.is_possible_number(phonenumbers.parse(phone_number)):
                raise CustomerPhoneNumberIsInvalid()
        except phonenumbers.NumberParseException as e:
            if e.error_type == phonenumbers.NumberParseException.INVALID_COUNTRY_CODE:
                raise CustomerPhoneNumberIsInvalid("The phone number is specified with invalid country code.")
            raise CustomerPhoneNumberIsInvalid()
