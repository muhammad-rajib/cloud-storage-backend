from sqlalchemy import (
    Column, Integer, String,
    ForeignKey, Boolean, TIMESTAMP
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from enum import IntEnum
from app.core.database import Base


class Storage(Base):
    __tablename__ = 'storages'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, index=True, default=None)
    user_id = Column(Integer, index=True, default=None)
    name = Column(String, nullable=False)
    total_size = Column(Integer)
    total_usage = Column(Integer, default=0)
    is_notification_enable = Column(Boolean, default=False)


class Bucket(Base):
    __tablename__ = 'buckets'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    storage_id = Column(Integer, ForeignKey('storages.id'), nullable=False)


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    location = Column(String(255), nullable=False)
    type = Column(Integer, nullable=False)
    extension = Column(Integer, nullable=True)
    size = Column(Integer, nullable=True)
    creation = Column(
        TIMESTAMP(timezone=True), server_default=func.now())
    owner_id = Column(Integer, nullable=False)


class Folder(Base):
    __tablename__ = 'folders'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    creation = Column(
        TIMESTAMP(timezone=True), server_default=func.now())
    last_modified = Column(
        TIMESTAMP(timezone=True), onupdate=func.now(), server_default=func.now())
    owner_id = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    updated_by = Column(Integer)


class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    item_id = Column(Integer, nullable=False)
    item_type = Column(Integer, nullable=False)
    item_name = Column(String(255), nullable=False)
    owner_id = Column(Integer, nullable=False)
    item_parent_id = Column(Integer)
