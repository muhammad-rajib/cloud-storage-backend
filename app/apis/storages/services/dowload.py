import os
from fastapi import status
from fastapi.responses import JSONResponse, FileResponse
from app.core.config import settings


def download_content(storage_name, filepath):
    abs_filepath = os.path.join(
        settings.ROOT_STORAGE_DIR, storage_name, filepath)

    if not os.path.exists(abs_filepath):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": "Content not found !"}
        )

    return FileResponse(path=abs_filepath)
