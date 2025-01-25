import logging
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from domuwa.auth import services
from domuwa.auth.models import TokenData, User
from domuwa.auth.security import verify_password
from domuwa.config import settings
from domuwa.database import get_db_session

logger = logging.getLogger(__name__)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CredentialsException = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def authenticate_user(username: str, password: str, session: Session):
    user = await services.get_by_username(username, session)
    if user is None:
        logger.debug("%s(username=%s) not found", User.__name__, username)
        return False
    if not verify_password(password, user.hashed_password):
        logger.debug("%s(username=%s) incorrect password", User.__name__, username)
        return False
    return user


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)],
):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.HASH_ALGORITHM],
        )
    except jwt.InvalidTokenError:
        raise CredentialsException

    username: str = payload.get("sub")
    if username is None:
        raise CredentialsException

    token_data = TokenData(username=username)
    user = await services.get_by_username(token_data.username, session)  # type: ignore
    if user is None:
        raise CredentialsException

    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user)],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )

    return current_user


async def get_admin_user(
    admin_user: Annotated[User, Security(get_current_active_user)],
):
    if not admin_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )

    return admin_user
