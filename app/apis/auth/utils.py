from passlib.context import CryptContext
from app.core.database import SessionLocal
from .models import RevokedToken


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


async def revoked_token(token: str):
    db = SessionLocal()
    # Check if the token is already revoked
    if db.query(RevokedToken).filter(RevokedToken.token == token).first():
        db.close()
        return
    # Add the token to the revoked tokens table
    revoked_token = RevokedToken(token=token)
    db.add(revoked_token)
    db.commit()
    db.close()
    print(f"Token revoked: {token}")
    return {"message": "Token revoked!"}
