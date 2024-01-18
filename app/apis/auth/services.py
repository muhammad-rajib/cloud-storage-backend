from fastapi.exceptions import HTTPException
from app.apis.users.services import get_user_detail
from .utils import get_password_hash, verify_password


async def change_user_password(user_id, data, current_user, db):
    user = get_user_detail(user_id, db)

    if current_user.id != user_id:
        raise HTTPException(
            status_code=403, detail="You are not allowed to change the password")

    if not verify_password(plain_password=data.current_password, hashed_password=user.password):
        raise HTTPException(
            status_code=401, detail="Incorrect Password !")

    new_hashed_password = get_password_hash(data.new_password)
    user.password = new_hashed_password

    db.commit()
    db.refresh(user)
    return {"message": "Password updated successfully !"}


def forget_password(email: str, db):
    return ''
