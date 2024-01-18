from datetime import datetime
from sqlalchemy import Column, String, Integer, Date, DateTime, Boolean, ForeignKey
from app.core.base_model import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    alt_email = Column(String(100))
    last_name = Column(String(100))
    first_name = Column(String(100))
    dob = Column(Date())
    contact_no = Column(String(20), index=True)
    alt_contact_no = Column(String(20))
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=True)
    blocked = Column(Boolean, default=False)
    inactive = Column(Integer, default=0)
    deleted = Column(Boolean, default=False)
    created = Column(DateTime(), default=datetime.utcnow())
    updated = Column(DateTime(), onupdate=datetime.utcnow())
    created_by = Column(Integer)
    updated_by = Column(Integer)
    email_verified = Column(Boolean, default=False)
    alt_email_verified = Column(Boolean, default=False)
    user_type = Column(Integer())
