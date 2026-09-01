from datetime import datetime
from enum import Enum

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """Available user roles."""

    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"


class UserRegister(BaseModel):
    """Schema for user registration."""

    name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )

    role: UserRole

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Vincent Mumo",
                "email": "vincent.mumo@example.com",
                "password": "StrongPassw0rd!",
                "role": "admin",
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login."""

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        max_length=128,
    )


class UserResponse(BaseModel):
    """Schema returned for a user."""

    id: str
    name: str
    email: EmailStr
    role: UserRole
    created_at: datetime


class Token(BaseModel):
    """Authentication token response."""

    access_token: str
    token_type: str = "bearer"
    expires_in_minutes: int


class TokenPayload(BaseModel):
    """Decoded JWT payload."""

    sub: str
    email: EmailStr
    role: UserRole
    exp: datetime