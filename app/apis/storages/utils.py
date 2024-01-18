import os
import mimetypes
from ..enums import FileTypeEnum


def avoid_duplicate_dirs(file_path):
    base, ext = os.path.splitext(file_path)
    counter = 1

    while os.path.exists(file_path):
        file_path = f"{base} ({counter}){ext}"
        counter += 1

    return file_path


def get_folder_size(folder_path):
    total_size = 0

    for dirpath, dirnames, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            total_size += os.path.getsize(file_path)

    # Convert bytes to megabytes
    total_size_mb = total_size / (1024 * 1024)

    return total_size_mb


def get_file_type_from_mime(mime_type):
    # Define MIME type mappings based on expected file types for cloud storage
    mime_mapping = {
        'image/jpeg': FileTypeEnum.IMAGE,
        'image/png': FileTypeEnum.IMAGE,
        'image/gif': FileTypeEnum.IMAGE,
        'image/bmp': FileTypeEnum.IMAGE,
        'image/tiff': FileTypeEnum.IMAGE,
        'image/webp': FileTypeEnum.IMAGE,
        'application/pdf': FileTypeEnum.DOCUMENT,
        'application/msword': FileTypeEnum.DOCUMENT,
        'application/vnd.ms-excel': FileTypeEnum.DOCUMENT,
        'application/vnd.ms-powerpoint': FileTypeEnum.DOCUMENT,
        'application/rtf': FileTypeEnum.DOCUMENT,
        'application/xml': FileTypeEnum.DOCUMENT,
        'application/json': FileTypeEnum.DOCUMENT,
        'audio/mpeg': FileTypeEnum.AUDIO,
        'audio/wav': FileTypeEnum.AUDIO,
        'audio/ogg': FileTypeEnum.AUDIO,
        'audio/midi': FileTypeEnum.AUDIO,
        'audio/x-flac': FileTypeEnum.AUDIO,
        'video/mp4': FileTypeEnum.VIDEO,
        'video/webm': FileTypeEnum.VIDEO,
        'video/quicktime': FileTypeEnum.VIDEO,
        'video/x-msvideo': FileTypeEnum.VIDEO,
        'video/x-matroska': FileTypeEnum.VIDEO,
        'application/zip': FileTypeEnum.OTHER,
        'application/x-gzip': FileTypeEnum.OTHER,
        'text/plain': FileTypeEnum.OTHER,
        'text/html': FileTypeEnum.OTHER,
        'text/css': FileTypeEnum.OTHER,
        'text/xml': FileTypeEnum.OTHER,
    }
    return mime_mapping.get(mime_type, FileTypeEnum.UNKNOWN)


def get_file_info(file_path):
    # Get file size
    file_size = os.path.getsize(file_path)

    # Get file extension
    _, file_extension = os.path.splitext(file_path)
    file_extension = file_extension.upper()

    # Get file type using mimetypes
    file_type, _ = mimetypes.guess_type(file_path)
    if file_type:
        file_type = get_file_type_from_mime(file_type)
    else:
        file_type = FileTypeEnum.UNKNOWN

    return {
        "file_size": file_size,
        "file_extension": file_extension.upper(),
        "file_type": file_type.value,
    }
