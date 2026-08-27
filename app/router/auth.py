from app.utils.auth import create_access_token, get_current_user

router = APIRouter(prefix="api/v1/auth", tags=["Authentication"])

@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
    summary="Register a new user",
    description="Create a new user account with a hashed password.Email must be unique."
)
async def register(payload: UserRegister)->UserResponse:
    """
    Register a new user with a hashed password.
    """
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )

    hashed = hash_password(payload.password)
    try:
        user_doc = user_model.create_user(
            name=payload.name,
            email=payload.email,    
            hashed_password=hashed,
            role=payload.role.value,
        )
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already exists",
        )
    return UserResponse(**user_model.serialize_user(user_doc))

@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="Login a user",
    description="Authenticate a user and return an access token."
)
async def login(payload: UserLogin)->Token:
    user_doc = user_model.get_user_by_email(payload.email)
    if user_doc is None or not Verify_password(payload.password, user_doc["hashed_password"]):
        raise HTTPException(
            status code=status.HTTP_401_UAUTHORIZED,
            detail="Invalid email or password",
            haeders={WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        subject=str(user_doc["_id"]),
        email=user_doc["email"],
        role=user_doc["role"],
    )
    return Token(
        access_tokens=access_token,
        token_type="bearer",
        expires_in_minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES,
    )
@router.get(
    "/me",
    response_model=UserResonse,
    summary="Get the current authenticated user",
    description="Returns the profile of the user identified by the bearer token."
)
async def get_me(current_user: dict=Depends(get_current_user))->UserResponse:
    return UserResponse(**user_model.serialized_user(current_user))