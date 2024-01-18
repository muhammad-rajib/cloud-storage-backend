from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.oauth import get_current_user
from app.apis.clients.schemas.client import ClientSetupCreate
from app.apis.users.models import User
from app.apis.clients.services.client import (
    add_new_client_setup,
    get_client_connection_info
)


router = APIRouter()


@router.post("/new-setup/add", response_model=ClientSetupCreate)
async def new_client_setup_api(
    payload: ClientSetupCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.user_type != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this resource.",
        )
    return add_new_client_setup(payload=payload, db=db)


@router.get("/connection-info/{client_id}")
async def client_connection_info_api(client_id: int, db: Session = Depends(get_db)):
    return get_client_connection_info(client_id=client_id, db=db)


@router.post("/test-storage-connection")
async def validate_client_connection():
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content="Connection Successfull !"
    )
