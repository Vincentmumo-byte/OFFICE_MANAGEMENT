from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.config import settings
from app.models import user_model
from app.schema.user_schema import (
    Token,
    UserLogin,
    UserRegister,
    UserResponse,
)
from app.utils.auth import (
    create_access_token,
    get_current_user,
)
from app.utils.password import (
    hash_password,
    verify_password,
)


router = APIRouter(
    prefix="/api/v1/auth",
    tags=["Authentication"],
)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
)
async def register(
    payload: UserRegister,
) -> UserResponse:

    existing_user = user_model.get_user_by_email(
        payload.email
    )

    if existing_user is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hashed = hash_password(
        payload.password
    )

    try:
        user_doc = user_model.create_user(
            name=payload.name,
            email=str(payload.email),
            hashed_password=hashed,
            role=payload.role.value,
        )

    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    return UserResponse(
        **user_model.serialize_user(user_doc)
    )


@router.post(
    "/login",
    response_model=Token,
)
async def login(
    payload: UserLogin,
) -> Token:

    user_doc = user_model.get_user_by_email(
        payload.email
    )

    if (
        user_doc is None
        or not verify_password(
            payload.password,
            user_doc["hashed_password"],
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={
                "WWW-Authenticate": "Bearer"
            },
        )

    access_token = create_access_token(
        subject=str(user_doc["_id"]),
        email=user_doc["email"],
        role=user_doc["role"],
    )

    return Token(
        access_token=access_token,
        token_type="bearer",
        expires_in_minutes=(
            settings.ACCESS_TOKEN_EXPIRE_MINUTES
        ),
    )


@router.get(
    "/me",
    response_model=UserResponse,
)
async def get_me(
    current_user: dict = Depends(
        get_current_user
    ),
) -> UserResponse:

    return UserResponse(
        **user_model.serialize_user(
            current_user
        )
    )