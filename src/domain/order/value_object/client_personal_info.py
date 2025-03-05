from dataclasses import dataclass

from dw_shared_kernel import ValueObject


@dataclass(kw_only=True, slots=True)
class ClientPersonalInformation(ValueObject):
    name: str
    email: str
    phone_number: str

    @classmethod
    def new(
        cls,
        name: str,
        email: str,
        phone_number: str,
    ) -> "ClientPersonalInformation": ...

    @staticmethod
    def _check_name(name: str) -> None: ...

    @staticmethod
    def _check_email(email: str) -> None: ...

    @staticmethod
    def _check_phone_number(phone_number: str) -> None: ...
