import os
import secrets
from functools import lru_cache
from typing import Optional, Dict, Any, List
from pydantic import PostgresDsn, validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # load data from .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True
    )
    PROJECT_NAME: str = None
    API_V1_STR: str = ""

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    # 60 minutes * 24 hours * 3 days = 3 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 3

    # application
    host: str
    port: str

    NO_AUTH_REQUIRED: List[str] = [
        '/',
        '/docs',
        '/openapi.json',
        '/login',
        '/logout',
        '/signup',
        '/send-email',
        '/verify_email',
        '/forget-password',
        '/reset-password',
        '/recovery-password'
    ]

    # backend
    CORS_ORIGINS: List[str] = [
        "http://localhost:8000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:8001"
    ]

    # cloudStorage DIR
    ROOT_STORAGE_NAME: Optional[str] = None
    DEFAULT_ROOT_STORAGE_NAME: Optional[str] = "CloudStorageVolt"

    @validator("ROOT_STORAGE_NAME")
    def get_root_storage_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if isinstance(v, str):
            return v
        return values.get("DEFAULT_ROOT_STORAGE_NAME")

    ROOT_STORAGE_DIR: str = None

    @validator("ROOT_STORAGE_DIR", pre=True)
    def update_root_storage_dir(v: Optional[str], values: Dict[str, Any]) -> str:
        os_user_dir = os.path.expanduser("~")
        storage_name = values.get('ROOT_STORAGE_NAME')
        if not storage_name:
            storage_name = values.get('DEFAULT_ROOT_STORAGE_NAME')
        update_root_storage_dir = os.path.join(os_user_dir, storage_name)
        return update_root_storage_dir

    # postgres
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    # Email
    EMAIL_SMTP_TLS: bool = True
    EMAIL_SMTP_PORT: Optional[int] = None
    EMAIL_SMTP_SERVER: Optional[str] = None
    EMAIL_SMTP_USER: Optional[str] = None
    EMAIL_SMTP_PASSWORD: Optional[str] = None
    EMAILS_FROM_EMAIL: Optional[str] = None
    EMAILS_FROM_NAME: Optional[str] = None

    @validator("EMAILS_FROM_NAME")
    def get_project_name(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        if not v:
            return values.get("PROJECT_NAME")
        return v

    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAIL_TEMPLATES_DIR: str = ""
    EMAILS_ENABLED: bool = True


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()
