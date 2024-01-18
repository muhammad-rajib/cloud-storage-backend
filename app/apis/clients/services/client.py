# fastapi
from fastapi import Depends, HTTPException, status
from fastapi.responses import JSONResponse
# sqlalchemy
from sqlalchemy import select
from sqlalchemy.orm import Session
# database
from app.core.database import get_db
# schemas
from app.apis.clients.schemas.client import ClientCreate, ClientSetupCreate
# models
from ..models.client import Client
from ..models.address import Address
from ..models.poc import PointOfContact
from ..models.app_registry import AppRegistry
from app.apis.storages.models import Storage
# services
from app.apis.users.services import create_new_user
from app.apis.storages.services.storage import setup_new_storage
from app.apis.clients.services.app_registry import create_new_app_registry


def get_client_info(api_client_secret, db: Session = Depends(get_db)):
    client_id = db.query(
        AppRegistry.__getattribute__(AppRegistry, client_id)
        .filter(AppRegistry.api_client_secret == api_client_secret)).first()
    storage_info_query = select(Storage.name).where(
        Storage.client_id == client_id)
    storage_name = db.execute(storage_info_query).scalar()
    return {
        'client_id': client_id,
        'storage_name': storage_name,
    }


def create_new_client(payload: ClientCreate, db, db_flush=False):
    db_client = Client(
        name=payload.name,
        company_code=payload.company_code,
        email=payload.email,
        phone=payload.phone,
        website=payload.website,
    )
    db.add(db_client)
    db.flush()

    db_address = Address(
        **payload.address.dict(),
        client_id=db_client.id
    )
    db_poc = PointOfContact(
        **payload.point_of_contacts.dict(),
        client_id=db_client.id
    )

    db.add(db_address)
    db.add(db_poc)

    if db_flush:
        db.flush()
        return db_client

    db.commit()
    db.refresh(db_address)
    db.refresh(db_poc)
    return db_client


def add_new_client_setup(payload, db):
    try:
        # retriev data
        client_setup_data = ClientSetupCreate(**payload.dict())
        with db.begin():
            # step-01: create new client > address:poc
            new_client = create_new_client(
                client_setup_data.client, db, db_flush=True)

            # step-02: create new user
            client_user = client_setup_data.user
            client_user = client_user.dict()
            client_user.update({'client_id': new_client.id})
            new_user = create_new_user(client_user, db, db_flush=True)

            # step-03: setup storage and bucket
            client_storage = client_setup_data.storage.dict()
            client_bucket = client_setup_data.storage.bucket.dict()
            client_storage.update({'client_id': new_client.id})
            new_storage_setup = setup_new_storage(
                client_user=new_user,
                storage=client_storage,
                bucket=client_bucket,
                db=db,
                db_flush=True
            )

            # step-04: prepare app_registry
            new_app_registry = create_new_app_registry(
                new_client.id, db, db_flush=True)

        db.commit()
        return JSONResponse(
            status_code=status.HTTP_201_CREATED,
            content={
                "client_id": new_client.id,
                "message": "New client setup completed successfully!"
            }
        )
    except Exception as e:
        db.rollback()
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'error': str(e),
                'message': "Failed to setup new client!"
            })


def get_client_connection_info(client_id, db):
    """
    client_id
    api_client_secret
    api_access_identification_key
    storage_name
    default_bucket_name
    """
    client_secrets = db.query(AppRegistry.api_client_secret, AppRegistry.api_access_identification_key).filter(
        AppRegistry.client_id == client_id).first()
    client_storage = db.query(Storage.name).filter(
        Storage.client_id == client_id).first()
    return {
        'client_id': client_id,
        'api_client_secret': client_secrets.api_client_secret,
        'api_access_identification_key': client_secrets.api_access_identification_key,
        'storage_name': client_storage.name,
        'default_bucket_name': 'DEFAULT_BUCKET'
    }
