"""Data_access functions for user-related operations in MongoDB."""
from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId

from pymongo.errors import DuplicateKeyError

def serialize_user(user_doc: dict) -> dict:
    """Serialize a user document from MongoDB to a dictionary."""
    return {
        "id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc["role"],
        "created_at": user_doc["created_at"]
    }

def create_user(name:str,email:str,hashed_password:str,role:str)->dict:
    """insert a new user document.Raise DuplicateKeyError if a user with the same email already exists.k    ey"""
    document = {
        "name": name,
        "email": email,
        "hashed_password": hashed_password,
        "role": role,
        "created_at": datetime.now(timezone.utc)
    }
    try:
        result = user_collection.insert_one(document)
    except DuplicateKeyError:
        raise 
    document["_id"] = result.inserted_id
    return document
def get_user_by_email(email:str)->Optional[dict]:
    """retrieve a user document by email from MongoDB"""
    return users_collection.find_one({"email": email.lower()})

def get_user_by_id(user_id:str)->Optional[dict]:
    """retrieve a user document by id from MongoDB"""
    try:
        object_id = ObjectId(user_id)
    except(InvalidId,TypeError):
        return None
    return user_collection.find_one({"_id": object_id})


