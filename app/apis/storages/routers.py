from typing import List
from fastapi import (
    APIRouter, Request, Form, File, Depends,
    UploadFile, HTTPException, status,
)
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.apis.users.services import get_client_admin_user
from app.apis.storages.services.upload import upload_content
from app.apis.storages.services.dowload import download_content
from app.apis.storages.services.storage import get_client_storage_info, get_user_storage_info
from app.apis.storages.schemas import DownloadRequest


router = APIRouter()


@router.post("/upload")
async def upload_content_api(
    request: Request,
    files: List[UploadFile] = File(...),
    store_path: str = Form(default=None),
    bucket_name: str = Form(default=None),
    db: Session = Depends(get_db)
):
    if not files:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "error": {
                    "message": "No file/content sent",
                    "description": "Provide file/content with request to store"
                }
            }
        )

    owner_id = ''
    # storage info
    storage_info = ''
    request_user_type = request.headers.get('user-type')
    if request_user_type == 'app':
        client_id = request.headers.get('client-id')
        storage_info = get_client_storage_info(int(client_id), db)
        onwer_id = get_client_admin_user(client_id, db)

    if request_user_type == 'user':
        user_id = request.headers.get('user-id')
        storage_info = get_user_storage_info(int(user_id), db)
        owner_id = user_id

    if not storage_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Storage not found!"
        )

    return await upload_content(
        files=files,
        path=store_path,
        storage_name=storage_info.name,
        bucket_name=bucket_name,
        owner_id=onwer_id,
        db=db
    )


@router.post("/download")
async def download_content_api(
    request: Request,
    payload: DownloadRequest,
    db: Session = Depends(get_db)
):
    filepath = payload.filepath
    if not filepath:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Filepath missing !"}
        )

    # storage info
    storage_info = ''
    request_user_type = request.headers.get('user-type')
    if request_user_type == 'app':
        client_id = request.headers.get('client-id')
        storage_info = get_client_storage_info(int(client_id), db)

    if request_user_type == 'user':
        user_id = request.headers.get('user-id')
        storage_info = get_user_storage_info(int(user_id), db)

    if not storage_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Storage not found!"
        )

    return download_content(storage_info.name, filepath)


@router.post("/download/multiple")
async def download_multiple_content_api(payload):
    pass
