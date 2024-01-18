from sqlalchemy import Column, String, Integer
from app.core.base_model import Base


class RevokedToken(Base):
    __tablename__ = "revoked_tokens"
    id = Column(Integer, primary_key=True, index=True,
                autoincrement=True, nullable=True)
    token = Column(String, unique=True, index=True)
