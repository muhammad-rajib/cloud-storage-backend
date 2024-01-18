from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.base_model import Base


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    client_id = Column(Integer, ForeignKey('clients.id'), nullable=False)
    country = Column(String, nullable=True)
    division = Column(String, nullable=True)
    city = Column(String, nullable=True)
    post_office = Column(String, nullable=True)
    post_code = Column(String, nullable=True)
    section = Column(String, nullable=True)
    road = Column(String, nullable=True)
    house = Column(String, nullable=True)

    clients = relationship("Client", back_populates="address")
