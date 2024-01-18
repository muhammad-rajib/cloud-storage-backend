from pydantic import BaseModel, EmailStr
from ..enums import UserTypeEnum


class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    password: str
    email: EmailStr
    user_type: UserTypeEnum


class UserResponse(BaseModel):
    id: int
    username: str
