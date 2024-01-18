from ..models.address import Address


def create_new_address(address, db, db_commit=True):
    new_address = Address(address.model_dump())
    db.add(new_address)
    if db_commit:
        db.commit()
    return new_address
