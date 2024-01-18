import secrets
import string
from .models.app_registry import AppRegistry


def generate_api_client_secret(length=32, db=None):
    while True:
        new_api_client_secret = secrets.token_urlsafe(32)
        if not db.query(AppRegistry).filter(AppRegistry.api_client_secret == new_api_client_secret).first():
            return new_api_client_secret


def generate_api_access_identification_key(length=32, db=None):
    while True:
        new_api_access_identification_key = secrets.token_urlsafe(32)
        if not db.query(AppRegistry).filter(
                AppRegistry.api_access_identification_key == new_api_access_identification_key).first():
            return new_api_access_identification_key
