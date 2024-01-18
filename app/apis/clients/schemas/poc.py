from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints


class POCSchema(BaseModel):
    # POC: point of contact person
    name: str
    department: str | None = None
    designation: str | None = None
    gender: str
    phone: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=8, max_length=15)]
    email: EmailStr
