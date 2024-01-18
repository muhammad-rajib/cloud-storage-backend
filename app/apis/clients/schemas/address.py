from pydantic import BaseModel


class AddressSchema(BaseModel):
    country: str
    division: str
    city: str
    post_office: str
    post_code: str
    section: str | None = None
    road: str | None = None
    house: str | None = None
