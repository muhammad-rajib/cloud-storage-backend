from fastapi import FastAPI, Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from app.core import oauth
from app.core.database import SessionLocal
from app.core.config import settings
from app.apis.auth.models import RevokedToken
from app.apis.clients.models.app_registry import AppRegistry


class RequestAuthenticationMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI):
        super().__init__(app)
        self.db = SessionLocal()

    async def dispatch(self, request: Request, call_next):

        if request.url.path in settings.NO_AUTH_REQUIRED:
            response = await call_next(request)
            return response

        user_type = request.headers.get('user-type', '')
        if not request.url.path in settings.NO_AUTH_REQUIRED and not user_type:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content={"message": "Invalid Request. May User type missing !"}
            )

        if user_type == 'app' and request.url.path not in settings.NO_AUTH_REQUIRED:
            is_request_validate, client_id = self.is_request_authenticate(
                request)
            if not is_request_validate:
                return JSONResponse(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    content={"message": "Invalid Access Credentials!"}
                )

            new_headers = request.headers.mutablecopy()
            new_headers.append('client-id', str(client_id))
            request._headers = new_headers
            response = await call_next(request)
            return response

        elif user_type == 'user' and request.url.path not in settings.NO_AUTH_REQUIRED:
            try:
                authorization_header = request.headers.get("Authorization")
                if authorization_header is None or "Bearer " not in authorization_header:
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Access Credentials!",
                        headers={"WWW-Authenticate": "Bearer"},
                    )
                token = authorization_header.replace("Bearer ", "")

                if self.is_token_revoked(token):
                    raise HTTPException(
                        status_code=status.HTTP_401_UNAUTHORIZED,
                        detail="Invalid Access Credentials!",
                        headers={"WWW-Authenticate": "Bearer"},
                    )

                user = await oauth.get_current_user(token)
                new_headers = request.headers.mutablecopy()
                new_headers.append('user-id', str(user.id))
                request._headers = new_headers
                response = await call_next(request)
                return response
            except HTTPException as e:
                return JSONResponse(
                    status_code=e.status_code,
                    content={"message": str(e.detail)}
                )

    def is_request_authenticate(self, request, is_authenticate=False):
        api_client_secret = request.headers.get('api-client-secret', '')
        api_access_identification_key = request.headers.get(
            'api-access-identification-key', '')
        app_registry_info = self.db.query(AppRegistry).filter(
            AppRegistry.api_client_secret == api_client_secret).first()
        self.db.close()

        if app_registry_info and app_registry_info.api_client_secret == api_client_secret \
                and app_registry_info.api_access_identification_key == api_access_identification_key:
            is_authenticate = True

        return is_authenticate, app_registry_info.client_id

    def is_token_revoked(self, token, is_revoked=False):
        revoked_token = self.db.query(RevokedToken.token).filter(
            RevokedToken.token == token).first()
        if revoked_token:
            is_revoked = True
        return is_revoked
