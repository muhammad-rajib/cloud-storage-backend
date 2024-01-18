from fastapi import status
from fastapi.exceptions import HTTPException
from app.apis.auth.utils import get_password_hash
from .schemas import UserCreate
from .models import User
from ..enums import UserTypeEnum


def get_user_type(username: str, db=None):
    query = db.query(User.user_type).filter(User.username == username).first()
    return query.user_type


def create_new_user(user: UserCreate, db=None, db_flush=False):
    if not isinstance(user, dict):
        user = user.model_dump()

    is_user_exist = db.query(User).filter(
        User.username == user.get('username')).first()
    if is_user_exist:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User already exists",
        )

    new_user = User(**user)
    new_user.password = get_password_hash(new_user.password)
    db.add(new_user)

    if db_flush:
        db.flush()
        return new_user

    db.commit()
    db.refresh(new_user)
    return new_user


def get_user_detail(id: int, db):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with this id {id} does not exist"
        )
    return user


def update_user_data(user: UserCreate, db):
    pass


def deactivate_user(id: int, db):
    user = get_user_detail(id, db)

    if user.inactive:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User already deactivated")

    user.inactive = 1
    db.commit()
    db.refresh(user)
    return user


def get_client_admin_user(client_id, db):
    client_admin = db.query(User.id).filter(
        User.client_id == client_id,
        User.user_type == UserTypeEnum.ADMIN.value
    ).first()
    return client_admin.id
