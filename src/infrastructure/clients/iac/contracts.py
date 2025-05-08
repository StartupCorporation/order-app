from pydantic import BaseModel


class GetAdminsEmailContract(BaseModel):
    emails: list[str]
