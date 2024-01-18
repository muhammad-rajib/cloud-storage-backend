from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.base_model import Base
from ..schemas.client import ClientCreate
from ..models.address import Address
from ..models.poc import PointOfContact


class Client(Base):
    __tablename__ = 'clients'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    company_code = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    website = Column(String, nullable=True)

    # Bidirectional relationship with Address table
    address = relationship('Address', back_populates='clients')

    # Bidirectional relationship with PointOfContacts table
    point_of_contacts = relationship(
        'PointOfContact', back_populates='clients')

    @classmethod
    def from_pydantic(cls, client_create: ClientCreate):
        return cls(
            name=client_create.name,
            email=client_create.email,
            phone=client_create.phone,
            website=client_create.website,
            address=Address(**client_create.address.dict()),
            point_of_contacts=PointOfContact(
                **client_create.point_of_contacts.dict())
        )
