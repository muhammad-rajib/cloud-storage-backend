from datetime import datetime
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime
from sqlalchemy.orm import relationship
from app.core.base_model import Base


class AppRegistry(Base):
    __tablename__ = 'app_registry'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    api_client_secret = Column(String(255), index=True, nullable=False)
    api_access_identification_key = Column(String(255), nullable=False)
    inactive = Column(Boolean, default=False,
                      nullable=False, server_default='0')
    deleted = Column(Boolean, default=False,
                     nullable=False, server_default='0')
    created = Column(DateTime(), default=datetime.utcnow())
    updated = Column(DateTime(), onupdate=datetime.utcnow())
    created_by = Column(Integer)
    updated_by = Column(Integer)
