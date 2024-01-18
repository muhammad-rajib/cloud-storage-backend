from fastapi import APIRouter
from app.apis.auth.routers import router as auth_router
from app.apis.users.routers import router as users_router
from app.apis.clients.routers import router as clients_router
from app.apis.storages.routers import router as storages_router
from app.apis.notifier.routers import router as notifier_router

api_router = APIRouter()


api_router.include_router(auth_router, tags=['Authentication'])
api_router.include_router(users_router, prefix="/users", tags=["Users"])
api_router.include_router(clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(
    storages_router, prefix="/storage", tags=["Storages"])
api_router.include_router(notifier_router, tags=["Notifier"])
