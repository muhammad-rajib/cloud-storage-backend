import os
from app.core.config import settings


def create_storage_dir(storage_name):
    try:
        new_dir = os.path.join(settings.ROOT_STORAGE_DIR, storage_name)
        os.mkdir(new_dir)
        return str(new_dir)
    except FileExistsError as e:
        raise Exception(
            "Storage Already Exist! Failed to create storage directory!")


def create_bucket_dir(storage_dir, bucket_name, initial_setup=False):
    try:
        if initial_setup:
            os.mkdir(os.path.join(storage_dir, 'DEFAULT_BUCKET'))
        new_dir = os.path.join(storage_dir, bucket_name)
        os.mkdir(new_dir)
        return str(new_dir)
    except FileExistsError as e:
        raise Exception("Failed to create bucket directory!")


def create_new_trash_dir(storage_dir):
    try:
        new_trash_dir = os.path.join(storage_dir, 'TRASH')
        os.mkdir(new_trash_dir)
        return str(new_trash_dir)
    except Exception as e:
        raise Exception("Failed to create trash directory!")
