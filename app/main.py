import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.middleware.auth import RequestAuthenticationMiddleware
from app.core.middleware.activity_log import ActivityLogMiddleware
from app.core.config import settings
from app.core.database import init_db
from app.apis.base_router import api_router


# APP INITIALIZATION
app = FastAPI()

# DB INITIALIZATION
init_db()


# MIDDLEWARES
# ==============================================
# Set all CORS enabled origins
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# custom middleware
app.add_middleware(ActivityLogMiddleware)
app.add_middleware(RequestAuthenticationMiddleware)
# ==============================================


# API ROUTES
# ==============================================
app.include_router(api_router, prefix=settings.API_V1_STR)

# ==============================================


if __name__ == "__main__":
    # start the server
    uvicorn.run(
        app,
        host=settings.host,
        port=settings.port
    )
