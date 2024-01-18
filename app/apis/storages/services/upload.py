import os
from app.core.config import settings
from ..utils import avoid_duplicate_dirs, get_file_info
from ..services.storage import (
    add_new_file_data,
    add_new_folder_data,
    add_new_item_data,
    get_last_node_item_id_from_path,
    get_matched_exist_path
)
from app.apis.enums import ItemTypeEnum


async def upload_content(files, path, storage_name, bucket_name, owner_id=None, db=None):
    """
    UPLOAD: upload content
    """
    path = str(path).replace('"', '') if path else None
    storage_name = str(storage_name).replace('"', '')
    bucket_name = str(bucket_name).replace('"', '') if bucket_name else None
    response_paths = []
    item_parent_id = ''

    # save content in provided path
    if path:
        store_path = os.path.join(
            settings.ROOT_STORAGE_DIR, storage_name, path)

        if not os.path.exists(store_path):
            # update parent id
            matched_path = get_matched_exist_path(store_path)
            item_parent_id = get_last_node_item_id_from_path(
                path=matched_path,
                owner_id=owner_id,
                db=db
            )
            new_dir = os.path.join(
                settings.ROOT_STORAGE_DIR, storage_name, path)
            os.makedirs(new_dir)

            # register into folders and items table
            new_items_path = os.path.join('/', storage_name, path)
            new_items_path = new_items_path.replace(matched_path, '')
            new_item_list = new_items_path.split('/')
            for item in new_item_list:
                new_item = add_new_folder_data(data={
                    'name': item,
                    'owner_id': owner_id,
                    'created_by': owner_id,
                    'updated_by': owner_id
                })

                item_model = add_new_item_data(data={
                    'item_id': new_item.id,
                    'item_name': new_item.name,
                    'item_type': ItemTypeEnum.FOLDER.value,
                    'owner_id': owner_id,
                    'item_parent_id': item_parent_id
                })
                item_parent_id = new_item.id

        if not item_parent_id:
            item_parent_id = get_last_node_item_id_from_path(
                path=os.path.join(settings.ROOT_STORAGE_DIR,
                                  storage_name, path),
                owner_id=owner_id,
                db=db
            )

        for file in files:
            file_content = file.file.read()
            filename = file.filename
            store_path = os.path.join(store_path, filename)

            if os.path.exists(store_path):
                store_path = avoid_duplicate_dirs(store_path)

            response_paths.append(store_path.replace(
                os.path.join(settings.ROOT_STORAGE_DIR, storage_name), ""))

            with open(store_path, "wb") as buffer:
                buffer.write(file_content)

            # update metadata
            file_metadata = get_file_info(store_path)
            file_model = add_new_file_data(data={
                'name': filename,
                'location': store_path.replace(settings.ROOT_STORAGE_DIR, ""),
                'type': file_metadata.get('file_type'),
                'extension': file_metadata.get('file_extension'),
                'size': file_metadata.get('file_size'),
                'owner_id': owner_id
            })

            item_model = add_new_item_data(data={
                'item_id': file_model.id,
                'item_name': file_model.name,
                'item_type': ItemTypeEnum.FILE.value,
                'owner_id': owner_id,
                'item_parent_id': item_parent_id
            })

        return {
            "path": response_paths
        }

    # save -> storage/default_bucket/
    # if bucket not specified
    if bucket_name == None:
        for file in files:
            file_content = file.file.read()
            filename = file.filename
            store_path = os.path.join(
                settings.ROOT_STORAGE_DIR, storage_name, 'DEFAULT_BUCKET', filename)

            if os.path.exists(store_path):
                store_path = avoid_duplicate_dirs(store_path)

            response_paths.append(store_path.replace(
                os.path.join(settings.ROOT_STORAGE_DIR, storage_name), ""))

            with open(store_path, "wb") as buffer:
                buffer.write(file_content)

        return {
            "path": response_paths
        }

    # save -> storage/bucket dir
    for file in files:
        file_content = file.file.read()
        filename = file.filename
        store_path = os.path.join(
            settings.ROOT_STORAGE_DIR, storage_name, bucket_name, filename)

        if os.path.exists(store_path):
            store_path = avoid_duplicate_dirs(store_path)

        response_paths.append(store_path.replace(
            os.path.join(settings.ROOT_STORAGE_DIR, storage_name), ""))

        with open(store_path, "wb+") as buffer:
            buffer.write(file_content)

        return {
            "path": response_paths
        }
