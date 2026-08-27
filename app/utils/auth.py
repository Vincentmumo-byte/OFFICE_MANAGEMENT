from datetime import datetime,timedelta, timezone
from typing import Optional, List

from fastapi import Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt,JWTError, ExpiredsignatureError
from pydantic import ValidationError

from app.config import settings
from app.schemas.user_schema import UserRole
from app.models import user_model

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/vi/auth/login",auto_error=False)

def creat_access_token(subject: str, email: str,role: str)->str:
    expire = datatime.now(timezone.utc) + timedelta(minutes= settings.ACESS_TOKEN_EXPIRE_MINUTES)
    payload = {
        "sub": subject,
        "email": email,
        "role": role,
        "exp": expire,
        "iat":datetime.now(timezone.utc)
    }
    return jwt.encode(payload, setting.JWT_SECRET_KEY,algorithm=settings.JWT_ALGORITHM)

def decode_access_token(token: str)->dict:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers {"www-Authenticate": "Bearer"},
    )
    expired_exception = HTTException(
        status_code =status.HTTP_401_UNAUTHORIZED,
        details ="Acess tokens has expired,please log in again"
        headers={"www-Authenticate":Bearer"}
    )
    try:
        payload =jwt.decode(token,settings.JWT_SECRETE_KEY,algorithms=[settings.JWT_ALLGORITHM])
        return payload
    except ExpiredSignatureError:
        raise expired_exception
    except JWTError:
        raise credential_exceptions

async def get_current_user(token: Optinal[str]=Depends(oauth2_scheme)) -> dict:
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_AUTHORIZED,
            detail="Invalid token payload",
            headers ={"www-Authenticate":"Bearer"}
        )
    user = user_model.get_user_by_id(user_id)
    if user is None:
         raise HTTPException(
            status_code=status.HTTP_401_AUTHORIZED,
            detail="Invalid token payload",
            headers ={"www-Authenticate":"Bearer"}
        )
    return user

def require_roles(allowed_roles: List[UserRole]):
    async def role_checker(current_user:dict = Depends(get_current_user))-> dict:
        user_role = current_user.get("role")
        allowed_values = [role.value for role in allowed_roles]
        if user_role not in allowed_values:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                details =f"Role'{user_role}'is not permitted to perform this action",
            )
        return current_user
    return role_checker    



