from fastapi import APIRouter, status, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.core import oauth
from app.core.database import get_db, SessionLocal
from app.apis.users.models import User
from .services import change_user_password, forget_password
from .schemas import ChangePassword, Token as UserToken
from .utils import revoked_token, verify_password


router = APIRouter()


@router.post("/login", response_model=UserToken)
async def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username ==
                                 user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Invalid Credentials"
        )

    if not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    encoded_jwt = oauth.create_access_token(
        data={'user_id': user.id, 'username': user.username})

    return {
        'access_token': encoded_jwt,
        'token_type': 'bearer'
    }


@router.post("/logout")
async def logout(token: str = Depends(oauth.oauth2_scheme)):
    await revoked_token(token)
    return {"message": "Logout successful"}


@router.put("/{user_id}/change-password")
async def change_user_password_api(
        user_id: int, data: ChangePassword,
        db: Session = Depends(get_db),
        current_user=Depends(oauth.get_current_user)):
    response = await change_user_password(user_id, data, current_user, db)
    return response


@router.post("/forget-password/{email}")
async def forget_password_api(
    email: str,
    db: Session = Depends(get_db)
):
    return forget_password(email=email, db=db)
