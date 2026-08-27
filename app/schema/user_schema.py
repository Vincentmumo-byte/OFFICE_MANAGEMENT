"""pydantic schemas for authentication and user -related requests/responses""" #RBAC
from datetime import datetime
from enum import Enum  

from pydantics import Basemodel, Emailstr,Field, ConfigDict 


class UserRole(str, Enum):
    """Enum class for user roles"""
    ADMIN = "admin"
    HR = "hr"
    EMPLOYEE = "employee"



class userRegister(Basemodel):
    """Schema for user registration"""
    name: str = Field(...,min_length=2,max_length=50,description="Name of the user")
    email: Emailstr = Field(...,description="Email of the user")
    password: str = Field(...,min_length=8,max_length=128,description="Password of the user")
    role: UserRole = Field(...,description="Role of the user")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Vincent Mumo",
                "email": "vincent.mumo@example.com",
                "password": "StrongPassw0rd!",
                "role": "admin"
            }
        }
    )



class UserLogin(Basemodel):
    """Schema for user login"""
    email: Emailstr = Field(...,description="Email of the user")
    password: str = Field(...,min_length=8,max_length=128,description="Password of the user")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "vincent.mumo@example.com",
                "password": "StrongPassw0rd!"
            }
        }
    )


class userResponse(Basemodel):
    """Schema for user response"""
    id: str = Field(...,description="MongoDB ObjectId as a string")
    name: str 
    email: Emailstr
    role: UserRole 
    created_at: datetime 

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "_id": "64b8f9e2f1c2a3b4d5e6f7g8",
                "name": "Vincent Mumo",
                "email": "vincent.mumo@example.com",
                "role": "admin",
                "created_at": "2023-07-21T10:00:00Z"
            }
        }
    )


class Token(Basemodel):
    """Response after succesful login"""
    access_token: str 
    token_type: str ="bearer"
    expires_in_minutes: int

    
class TokenPayload(Basemodel):
    """decoded contents of jwt access token"""
    sub: str 
    email: Emailstr
    role: UserRole 
    exp: datetime