"""Pydantic schemas for employee operations."""

import re
from datetime import date, datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
)


PHONE_REGEX = re.compile(
    r"^\+?\d{10,15}$"
)


class EmployeeCreate(BaseModel):
    """Schema for creating an employee."""

    first_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    second_name: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    email: EmailStr

    phone_number: Optional[str] = None

    department: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    designation: str = Field(
        ...,
        min_length=2,
        max_length=50,
    )

    salary: float = Field(
        ...,
        gt=0,
    )

    joining_date: date

    is_active: bool = True

    @field_validator(
        "first_name",
        "second_name",
        "department",
        "designation",
    )
    @classmethod
    def not_blank(cls, value: str):
        value = value.strip()

        if not value:
            raise ValueError(
                "Field cannot be blank"
            )

        return value

    @field_validator("phone_number")
    @classmethod
    def validate_phone_number(cls, value):
        if value is None:
            return value

        if not PHONE_REGEX.match(value):
            raise ValueError(
                "Invalid phone number format"
            )

        return value


class EmployeeUpdate(BaseModel):
    """Schema for updating an employee."""

    first_name: Optional[str] = None
    second_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone_number: Optional[str] = None
    department: Optional[str] = None
    designation: Optional[str] = None
    salary: Optional[float] = Field(
        None,
        gt=0,
    )
    joining_date: Optional[date] = None
    is_active: Optional[bool] = None


class EmployeeResponse(BaseModel):
    """Employee response schema."""

    id: str
    employee_id: str

    first_name: str
    second_name: str

    email: EmailStr
    phone_number: Optional[str] = None

    department: str
    designation: str

    salary: float
    joining_date: date

    is_active: bool

    profile_picture: Optional[str] = None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,
    )


class PaginatedEmployeeResponse(BaseModel):
    """Paginated employee response."""

    total: int
    page: int
    size: int
    employees: List[EmployeeResponse]