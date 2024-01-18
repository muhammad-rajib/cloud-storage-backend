from ..models import Bucket


def create_new_bucket(bucket, db, db_flush=False):
    new_bucket = Bucket(**bucket)
    db.add(new_bucket)

    if db_flush:
        db.flush()
        return new_bucket

    db.commit()
    db.refresh(new_bucket)
    return new_bucket
