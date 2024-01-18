import os
from fastapi.exceptions import HTTPException
from fastapi import status
from app.core.config import settings
from app.core.database import SessionLocal
from ..models import Storage
from ..services.bucket import create_new_bucket
from ..services.directory import (
    create_storage_dir,
    create_bucket_dir,
    create_new_trash_dir
)
from app.apis.storages.models import Storage
from app.apis.storages.models import (
    File as FileModel,
    Item as ItemModel,
    Folder as FolderModel
)
from app.apis.enums import ItemTypeEnum, FileExtensionTypeEnum, FileTypeEnum


def get_client_storage_info(client_id, db=None):
    storage_info = db.query(Storage).filter(
        Storage.client_id == client_id).first()
    return storage_info


def get_user_storage_info(user_id, db=None):
    storage_info = db.query(Storage).filter(
        Storage.client_id == user_id).first()
    return storage_info


def create_new_storage(storage, db, db_flush=False):
    new_storage = Storage(**storage)
    db.add(new_storage)

    if db_flush:
        db.flush()
        return new_storage

    db.commit()
    db.refresh(new_storage)
    return new_storage


def setup_new_storage(client_user, storage, bucket, db, db_flush=False):
    """
    Setup new storage in storage system
    1. store storage info into db
    2. create storage and bucket dir
    """
    # ROOT STORAGE SETUP
    del storage['bucket']
    new_storage = create_new_storage(storage, db, db_flush=db_flush)
    new_storage_dir = create_storage_dir(new_storage.name)

    new_folder_model = add_new_folder_data({
        'name': new_storage.name,
        'owner_id': client_user.id,
        'created_by': client_user.id,
        'updated_by': client_user.id
    })

    new_storage_item_model = add_new_item_data(data={
        'item_id': new_folder_model.id,
        'item_name': new_folder_model.name,
        'item_type': ItemTypeEnum.FOLDER.value,
        'owner_id': client_user.id
    })

    # CUSTOM BUCKET SETUP
    bucket['storage_id'] = new_storage.id
    new_bucket = create_new_bucket(bucket, db, db_flush=db_flush)
    new_bucket_dir = create_bucket_dir(
        new_storage_dir, new_bucket.name, initial_setup=True)

    new_bucket_folder_model = add_new_folder_data(data={
        'name': new_bucket.name,
        'owner_id': client_user.id,
        'created_by': client_user.id,
        'updated_by': client_user.id
    })

    new_item_bucket_model = add_new_item_data(data={
        'item_id': new_bucket_folder_model.id,
        'item_type': ItemTypeEnum.FOLDER.value,
        'item_name': new_bucket_folder_model.name,
        'owner_id': client_user.id,
        'item_parent_id': new_folder_model.id
    })

    # DEFAULT BUCKET SETUP
    new_default_bucket_folder_model = add_new_folder_data(data={
        'name': 'DEFAULT_BUCKET',
        'owner_id': client_user.id,
        'created_by': client_user.id,
        'updated_by': client_user.id
    })

    new_item_bucket_model = add_new_item_data(data={
        'item_id': new_default_bucket_folder_model.id,
        'item_type': ItemTypeEnum.FOLDER.value,
        'item_name': new_default_bucket_folder_model.name,
        'owner_id': client_user.id,
        'item_parent_id': new_folder_model.id
    })

    # TRASH SETUP
    new_trash_dir = create_new_trash_dir(new_storage_dir)
    new_trash_folder_model = add_new_folder_data({
        'name': 'TRASH',
        'owner_id': client_user.id,
        'created_by': client_user.id,
        'updated_by': client_user.id
    })

    new_trash_item_model = add_new_item_data(data={
        'item_id': new_trash_folder_model.id,
        'item_name': new_trash_folder_model.name,
        'item_type': ItemTypeEnum.FOLDER.value,
        'owner_id': client_user.id,
        'item_parent_id': new_storage_item_model.item_id
    })

    response = {
        'new_storage': new_storage,
        'new_storage_dir': new_storage_dir,
        'new_bucket': new_bucket,
        'new_bucket_dir': new_bucket_dir,
        'new_trash_dir': new_trash_dir
    }
    return response


def add_new_file_data(data):
    """
    # TODO
    # - add pydantic validation for data
    # - convert pydantic schema into python dic data model
    # - other code will be as it is
    """
    try:
        db = SessionLocal()
        new_file_model = FileModel(
            name=data.get('name'),
            location=data.get('location'),
            type=data.get('type'),
            extension=FileExtensionTypeEnum[data.get(
                'extension').replace('.', '')].value,
            size=data.get('size', ''),
            owner_id=data.get('owner_id')
        )
        db.add(new_file_model)
        db.commit()
        db.refresh(new_file_model)
        db.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert into files table."
        )

    return new_file_model


def add_new_folder_data(data):
    """
    # TODO
    # - add pydantic validation for data
    # - convert pydantic schema into python dic data model
    # - other code will be as it is
    """
    try:
        db = SessionLocal()
        new_folder_model = FolderModel(
            name=data.get('name'),
            owner_id=data.get('owner_id'),
            created_by=data.get('created_by'),
            updated_by=data.get('updated_by')
        )
        db.add(new_folder_model)
        db.commit()
        db.refresh(new_folder_model)
        db.close()
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert into folders table."
        )

    return new_folder_model


def add_new_item_data(data):
    """
    # TODO
    # - add pydantic validation for data
    # - convert pydantic schema into python dic data model
    # - other code will be as it is
    """
    try:
        db = SessionLocal()
        new_item_model = ItemModel(
            item_id=data.get('item_id'),
            item_type=data.get('item_type'),
            item_name=data.get('item_name'),
            owner_id=data.get('owner_id'),
            item_parent_id=data.get('item_parent_id', None)
        )
        db.add(new_item_model)
        db.commit()
        db.refresh(new_item_model)
        db.close()
        return new_item_model
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to insert into items table."
        )


def get_file_id(owner_id, file_name, db):
    file_id_query = db.query(FileModel.id).filter(
        FileModel.owner_id == owner_id, FileModel.name == file_name).first()
    return file_id_query.id


def get_folder_id(owner_id, folder_name, db):
    folder_id_query = db.query(FolderModel.id).filter(
        FolderModel.owner_id == owner_id, FolderModel.name == folder_name).first()
    return folder_id_query.id


def get_matched_parent_child_id(parent_id, child_folder_name, db):
    child_id_query = db.query(ItemModel.item_id).filter(
        ItemModel.item_parent_id == parent_id,
        ItemModel.item_name == child_folder_name
    ).first()
    return child_id_query.item_id


def get_last_node_item_id_from_path(path, owner_id, db):
    """
    # Expected path: /root/user/ OR /root/user OR /root/user/file.extension
    # Converted path (dirname): /root/user
    """
    path = path.replace(settings.ROOT_STORAGE_DIR, '')
    folder_list = path.split('/')
    folder_list = [value for value in folder_list if value]

    if len(folder_list) == 1:
        return get_folder_id(owner_id, folder_list[0], db)

    parent_folder_id = get_folder_id(owner_id, folder_list[0], db)
    for indx in range(1, len(folder_list)):
        child_id = get_matched_parent_child_id(
            parent_id=parent_folder_id, child_folder_name=folder_list[indx], db=db)
        parent_folder_id = child_id

    return parent_folder_id


def get_matched_exist_path(path):
    folder_list = path.split('/')
    folder_list = [value for value in folder_list if value]

    if len(folder_list) == 1:
        return path

    matched_path = os.path.join('/', folder_list[0])
    for indx in range(1, len(folder_list)):
        matched_path = os.path.join(matched_path, folder_list[indx])
        if not os.path.exists(matched_path):
            matched_path = matched_path.replace(folder_list[indx], '')
            matched_path = matched_path.replace(settings.ROOT_STORAGE_DIR, '')
            break

    return matched_path
