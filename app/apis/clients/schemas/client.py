from typing_extensions import Annotated
from pydantic import BaseModel, EmailStr, StringConstraints
from ..schemas.address import AddressSchema
from ..schemas.poc import POCSchema
from app.apis.storages.schemas import StorageCreate
from app.apis.users.schemas import UserCreate


class ClientCreate(BaseModel):
    name: str
    company_code: str
    email: EmailStr
    phone: Annotated[str, StringConstraints(
        strip_whitespace=True, min_length=8, max_length=15)]
    website: str | None = None
    address: AddressSchema
    point_of_contacts: POCSchema


class ClientSetupCreate(BaseModel):
    client: ClientCreate
    user: UserCreate
    storage: StorageCreate
