from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.core import oauth
from app.core.database import get_db
from app.apis.users.schemas import (
    UserCreate,
    UserResponse,
)
from app.apis.users.services import (
    create_new_user,
    get_user_detail,
    deactivate_user
)


router = APIRouter()


@router.get("/", response_model=list[UserResponse])
async def get_users_api(db: Session = Depends(get_db)):
    return ''


@router.post("/add", status_code=status.HTTP_201_CREATED, response_model=UserResponse)
async def add_user_api(user: UserCreate, db: Session = Depends(get_db)):
    return create_new_user(user, db)


@router.get("/{id}", response_model=UserResponse)
async def get_user_detail_api(
    id: int,
    db: Session = Depends(get_db),
    current_user=Depends(oauth.get_current_user)
):
    if current_user.id != id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"You are not allowed to view other user details!"
        )
    return get_user_detail(id, db)


@router.delete("/{id}/deactivate", response_model=UserResponse)
async def deactivate_user_api(id: int, db: Session = Depends(get_db)):
    return deactivate_user(id, db)
