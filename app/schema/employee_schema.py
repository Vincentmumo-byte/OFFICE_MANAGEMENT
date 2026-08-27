"""Pydantic schema for employee-related requests/responses"""
import re
from datetime import date,datetime
from typing import Optional,List

from pydantic import BaseModel, Field, EmailStr, field_validator, ConfigDict

PHOENE_REGEX = re.compile(r"^\+?\d{10,15}$")

class Employeecreate(Basemodel):
    """payload for creating a new employee"""
    first_name: str = Field(...,min_length=2,max_length=50,description="First name of the employee")
    second_name: str = Field(...,min_length=2,max_length=50,description="Second name of the employee")
    email: EmailStr = Field(...,description="Email of the employee")
    phone_number: Optional[str] = Field(None,description="Phone number of the employee")
    department: str = Field(...,min_length=2,max_length=50,description="Department of the employee")
    designation: str = Field(...,min_length=2,max_length=50,description="Designation of the employee")
    salary: float = Field(...,gt=0,description="Salary of the employee")
    joining_date: date = Field(...,description="Joining date of the employee")
    is_active: bool = Field(default=True,description="Indicates if the employee is active")

    @field_validator("first_name","second_name","department","designation") #strips whitespace and raises ValueError if blank
    def not_blank(cls,value):
        if not value.strip():
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("phone_number") #validates phone number format
    def validate_phone_number(cls,value):
        if value is None:
            return value
        if not PHOENE_REGEX.match(value):
            raise ValueError("Invalid phone number format,must contain 7-15 digits and can start with +")
        return value


model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "first_name": "John",
            "second_name": "Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "department": "Engineering",
            "designation": "Software Engineer",
            "salary": 75000.0,
            "joining_date": "2023-01-15"
        }
    }
)


class EmployeeUpdate(BaseModel):
    """payload for updating an existing employee"""
    first_name: Optional[str] = Field(None,min_length=2,max_length=50,description="First name of the employee")
    second_name: Optional[str] = Field(None,min_length=2,max_length=50,description="Second name of the employee")
    email: Optional[EmailStr] = Field(None,description="Email of the employee")
    phone_number: Optional[str] = Field(None,description="Phone number of the employee")
    department: Optional[str] = Field(None,min_length=2,max_length=50,description="Department of the employee")
    designation: Optional[str] = Field(None,min_length=2,max_length=50,description="Designation of the employee")
    salary: Optional[float] = Field(None,gt=0,description="Salary of the employee")
    joining_date: Optional[date] = Field(None,description="Joining date of the employee")
    is_active: Optional[bool] = Field(None,description="Indicates if the employee is active")

    @field_validator("first_name","second_name","department","designation") #strips whitespace and raises ValueError if blank
    def not_blank(cls,value):
        if value is not None and not value.strip():
            raise ValueError("Field cannot be blank")
        return value

    @field_validator("phone_number") #validates phone number format
    @classmethod
    def validate_phone_number(cls,value):
        if value is None:
            return value
        if not PHOENE_REGEX.match(value):
            raise ValueError("Invalid phone number format,must contain 7-15 digits and can start with +")
        return value

model_config = ConfigDict(
    json_schema_extra={ 
        "example":  {
            "first_name": "Jane"
        }



class EmployeeResponse(BaseModel):
    """Schema for employee response"""
    id: str = 
    first_name: str 
    second_name: str 
    email: EmailStr 
    phone_number: int 
    department: str 
    designation: str 
    salary: float 
    joining_date: date 
    is_active: bool
    profile_picture: Optional[str] = None
    created_at: datetime 
    updated_at: datetime 


model_config = ConfigDict(
    json_schema_extra={
        "example": {
            "id": "64b8f1e2c9e77a3f4d5e6b7c",
            "first_name": "Jane",
            "second_name": "Doe",
            "email": "jane.doe@example.com",
            "phone_number": "+1234567890",
            "department": "Marketing",
            "designation": "Marketing Manager",
            "salary": 85000.0,
            "joining_date": "2023-02-01",
            "is_active": True,
            "profile_picture": None,
            "created_at": "2023-01-15T10:00:00Z",
            "updated_at": "2023-01-15T10:00:00Z"
        }
    }
)

class PaginatedEmployeeResponse(BaseModel):
    """Schema for paginated employee response"""
    total: int = Field(...,description="Total number of employees")
    page: int = Field(...,description="Current page number")
    size: int = Field(...,description="Number of employees per page")
    employees: List[EmployeeResponse] = Field(...,description="List of employees on the current page")















