from fastapi import UploadFile, File
from fastapi import Query
from pydantic import BaseModel


class BucketCreate(BaseModel):
    name: str


class StorageCreate(BaseModel):
    name: str
    total_size: int
    is_notification_enable: bool | None = None
    bucket: BucketCreate


class DownloadRequest(BaseModel):
    filepath: str


class UploadDataCreate(BaseModel):
    file: UploadFile = File(...)
    path: str | None = None
    storage_name: str
    bucket_name: str | None = None


class UploadResponse(BaseModel):
    path: str
    filename: str
