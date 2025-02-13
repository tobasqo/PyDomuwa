import datetime as dt

import jwt
from fastapi import HTTPException, status
from passlib.context import CryptContext

from domuwa.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(data: dict, expires_delta: dt.timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = dt.datetime.now(dt.timezone.utc) + expires_delta
    else:
        expire = dt.datetime.now(dt.timezone.utc) + dt.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.HASH_ALGORITHM],
        )
        expire = payload.get("exp")
        if expire is not None:
            expire_time = dt.datetime.fromtimestamp(expire, tz=dt.timezone.utc)
            if expire_time < dt.datetime.now(dt.timezone.utc):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token has expired",
                )
        return payload
    except jwt.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
