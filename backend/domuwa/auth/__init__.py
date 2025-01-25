from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from sqlmodel import Session

from domuwa.auth import services
from domuwa.auth.models import TokenData, User
from domuwa.auth.security import verify_password
from domuwa.config import settings
from domuwa.database import get_db_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CredentialsException = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


async def authenticate_user(username: str, password: str, session: Session):
    user = await services.get_by_username(username, session)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


async def get_current_user(
    security_scopes: SecurityScopes,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)],
):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise CredentialsException

    username: str = payload.get("sub")
    if username is None:
        raise CredentialsException

    token_scopes = payload.get("scopes", [])
    token_data = TokenData(username=username, scopes=token_scopes)
    user = await services.get_by_username(token_data.username, session)
    if user is None:
        raise CredentialsException

    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )

    return user


async def get_current_active_user(
    current_user: Annotated[User, Security(get_current_user, scopes=["me"])],
):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive user"
        )


async def get_admin_user(
    admin_user: Annotated[User, Security(get_current_active_user, scopes=["me"])],
):
    if not admin_user.is_staff:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions"
        )
