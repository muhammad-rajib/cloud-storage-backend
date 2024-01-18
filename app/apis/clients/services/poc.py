from ..models.poc import PointOfContact


def create_new_poc(poc, db, db_commit=True):
    new_poc = PointOfContact(poc.model_dump())
    db.add(new_poc)
    if db_commit:
        db.commit()
    return new_poc
