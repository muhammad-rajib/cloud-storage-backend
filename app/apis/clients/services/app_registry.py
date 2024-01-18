from ..utils import (
    generate_api_client_secret,
    generate_api_access_identification_key
)
from ..models.app_registry import AppRegistry


def create_new_app_registry(client_id=None, db=None, db_flush=True):
    api_client_secret = generate_api_client_secret(db=db)
    api_access_identification_key = generate_api_access_identification_key(
        db=db)

    new_app_registry = AppRegistry(
        client_id=client_id,
        api_client_secret=api_client_secret,
        api_access_identification_key=api_access_identification_key
    )
    db.add(new_app_registry)

    if db_flush:
        db.flush()
        return new_app_registry

    db.commit()
    db.refresh(new_app_registry)
    return new_app_registry
