import logging
from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from domuwa import auth
from domuwa.auth import services
from domuwa.auth.models import Token, User, UserCreate, UserRead, UserUpdate
from domuwa.auth.security import create_access_token, decode_token
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


def check_same_user(user1: User, user2: User):
    for field in ("id", "username", "hashed_password", "is_active", "is_staff"):
        if getattr(user1, field) != getattr(user2, field):
            return False
    return True


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
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    access_token = create_access_token(
        {"sub": user.username},
        expires_delta=access_token_expires,
    )
    refresh_token = create_access_token(
        {"sub": user.username},
        expires_delta=refresh_token_expires,
    )

    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


# TODO: add tests
@router.post("/refresh")
async def refresh_access_token(refresh_token: str = Cookie(None)):
    if not refresh_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No refresh token",
        )

    payload = decode_token(refresh_token)
    username = payload.get("sub")

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token",
        )

    new_access_token = create_access_token(
        {"sub": username},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return Token(
        access_token=new_access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )

# TODO: convert below endpoints to class
@router.get("/me", response_model=UserRead)
async def read_user(current_user: Annotated[User, Depends(auth.get_current_user)]):
    return current_user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserRead)
async def create_user(
    user_create: UserCreate, session: Annotated[Session, Depends(get_db_session)]
):
    logger.debug("got %s(%s) to create", User.__name__, user_create)
    user = await services.create(user_create, session)
    if user is None:
        err_msg = f"{User.__name__}(username={user_create.username}) already exists"
        logger.error(err_msg)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=err_msg,
        )
    return user


@router.get("/", response_model=list[UserRead])
async def get_all_users(
    session: Annotated[Session, Depends(get_db_session)],
    _: Annotated[User, Depends(auth.get_current_active_user)],
):
    return await services.get_all(session)


@router.get("/{user_id}", response_model=UserRead)
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


@router.patch("/{user_id}", response_model=UserRead)
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
    is_same_user = check_same_user(current_user, user)
    if not (is_same_user or current_user.is_staff):
        raise HTTPException(
            status.HTTP_403_FORBIDDEN,
            "Not enough permissions",
        )
    return await services.update(user, user_update, session)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
async def delete_user(
    user_id: int,
    session: Annotated[Session, Depends(get_db_session)],
    _: Annotated[User, Depends(auth.get_admin_user)],
):
    logger.debug("got %s(id=%d) to mark as inactive", User.__name__, user_id)
    user = await get_user_or_404(user_id, session)
    return await services.delete(user, session)
