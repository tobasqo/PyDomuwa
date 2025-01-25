import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from domuwa import auth
from domuwa.auth import services
from domuwa.auth.models import Token, User, UserCreate, UserUpdate
from domuwa.auth.security import create_access_token
from domuwa.config import settings
from domuwa.database import get_db_session

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Authentication"])


async def get_user_or_404(user_id: int, session: Session):
    user = await services.get_by_id(user_id, session)
    if not user:
        err_msg = f"{User.__name__}(id={user_id}) not found"
        logger.error(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    return user


@router.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: Annotated[Session, Depends(get_db_session)],
):
    user = await auth.authenticate_user(form_data.username, form_data.password, session)
    if not user:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=access_token_expires,
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me")
async def read_user(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return current_user


@router.post("/")
async def create_user(
    user: UserCreate, session: Annotated[Session, Depends(get_db_session)]
):
    logger.debug("got %s(%s) to create", User.__name__, user)
    return await services.create(user, session)


@router.get("/")
async def get_all_users(
    session: Annotated[Session, Depends(get_db_session)],
    _: Annotated[User, Depends(auth.get_current_active_user)],
):
    return await services.get_all(session)


@router.get("/{user_id}")
async def get_user_by_id(
    user_id: int,
    session: Annotated[Session, Depends(get_db_session)],
    _: Annotated[User, Depends(auth.get_current_active_user)],
):
    logger.debug("got %s(id=%d) to get", User.__name__, user_id)
    user = await get_user_or_404(user_id, session)
    if not user.is_active:
        logger.warning("got %s(id=%d%s) to get, but is not active", user.username)
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"{User.__name__}(id={user_id}) not found)",
        )
    return user


@router.patch("/{user_id}")
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    session: Annotated[Session, Depends(get_db_session)],
    current_user: Annotated[User, Depends(auth.get_current_active_user)],
):
    logger.debug(
        "got %s(%s) to update %s(id=%d)",
        User.__name__,
        user_update,
        User.__name__,
        user_id,
    )
    user = await get_user_or_404(user_id, session)
    if user != current_user or not current_user.is_staff:
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Not enough permissions",
        )
    return await services.update(user, user_update, session)


@router.delete("/{user_id}")
async def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_db_session)],
    _: Annotated[User, Depends(auth.get_admin_user)],
):
    logger.debug("got %s(id=%d) to mark as inactive", User.__name__, user_id)
    user = await get_user_or_404(user_id, session)
    await services.delete(user, session)
