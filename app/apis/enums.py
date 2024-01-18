from enum import IntEnum


class UserTypeEnum(IntEnum):
    SUPER_ADMIN = 1
    ADMIN = 2
    GENERAL = 3


class FileTypeEnum(IntEnum):
    IMAGE = 1
    DOCUMENT = 2
    AUDIO = 3
    VIDEO = 4
    OTHER = 5
    UNKNOWN = 6


class ItemTypeEnum(IntEnum):
    FILE = 1
    FOLDER = 2


class FileExtensionTypeEnum(IntEnum):
    # Image Extensions
    JPG = 101
    JPEG = 102
    PNG = 103
    GIF = 104
    BMP = 105
    TIFF = 106

    # Document Extensions
    PDF = 201
    DOC = 202
    DOCX = 203
    XLS = 204
    XLSX = 205
    PPT = 206
    PPTX = 207
    TXT = 208

    # Audio Extensions
    MP3 = 301
    WAV = 302
    AAC = 303
    FLAC = 304
    OGG = 305

    # Video Extensions
    MP4 = 401
    AVI = 402
    MKV = 403
    WMV = 404
    MOV = 405

    # Other Extensions
    ZIP = 501
    GZ = 502

    # Disk Extensions
    DMG = 601
