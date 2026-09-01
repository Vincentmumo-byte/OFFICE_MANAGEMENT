"""Database operations for employees."""

from datetime import datetime, timezone
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId

from app.database.mongodb import employees_collection


ALLOWED_SORT_FIELDS = {
    "salary",
    "joining_date",
    "first_name",
    "second_name",
    "department",
    "designation",
}


def _next_employee_id() -> str:
    """Generate the next employee ID."""

    count = employees_collection.count_documents({})

    return f"EMP-{count + 1:04d}"


def serialize_employee(employee_doc: dict) -> dict:
    """Convert a MongoDB employee document into a dictionary."""

    return {
        "id": str(employee_doc["_id"]),
        "employee_id": employee_doc["employee_id"],
        "first_name": employee_doc["first_name"],
        "second_name": employee_doc["second_name"],
        "email": employee_doc["email"],
        "phone_number": employee_doc.get("phone_number"),
        "department": employee_doc["department"],
        "designation": employee_doc["designation"],
        "salary": employee_doc["salary"],
        "joining_date": employee_doc["joining_date"],
        "is_active": employee_doc["is_active"],
        "profile_picture": employee_doc.get(
            "profile_picture"
        ),
        "created_at": employee_doc["created_at"],
        "updated_at": employee_doc["updated_at"],
    }


def create_employee(data: dict) -> dict:
    """Create a new employee."""

    now = datetime.now(timezone.utc)

    document = {
        "employee_id": _next_employee_id(),
        "first_name": data["first_name"],
        "second_name": data["second_name"],
        "email": str(data["email"]).lower(),
        "phone_number": data.get("phone_number"),
        "department": data["department"],
        "designation": data["designation"],
        "salary": data["salary"],
        "joining_date": datetime.combine(
            data["joining_date"],
            datetime.min.time(),
        ),
        "is_active": True,
        "profile_picture": None,
        "created_at": now,
        "updated_at": now,
    }

    result = employees_collection.insert_one(document)

    document["_id"] = result.inserted_id

    return document


def get_employee_by_id(
    employee_id: str,
) -> Optional[dict]:

    try:
        object_id = ObjectId(employee_id)
    except (InvalidId, TypeError):
        return None

    return employees_collection.find_one(
        {"_id": object_id}
    )


def get_employee_by_email(
    email: str,
) -> Optional[dict]:

    return employees_collection.find_one(
        {"email": str(email).lower()}
    )


def update_employee(
    employee_id: str,
    update_data: dict,
) -> Optional[dict]:

    try:
        object_id = ObjectId(employee_id)
    except (InvalidId, TypeError):
        return None

    if "joining_date" in update_data:
        if update_data["joining_date"] is not None:
            update_data["joining_date"] = datetime.combine(
                update_data["joining_date"],
                datetime.min.time(),
            )

    if "email" in update_data:
        if update_data["email"] is not None:
            update_data["email"] = (
                str(update_data["email"]).lower()
            )

    update_data["updated_at"] = datetime.now(timezone.utc)

    employees_collection.update_one(
        {"_id": object_id},
        {"$set": update_data},
    )

    return employees_collection.find_one(
        {"_id": object_id}
    )


def set_profile_picture(
    employee_id: str,
    filename: str,
) -> Optional[dict]:

    try:
        object_id = ObjectId(employee_id)
    except (InvalidId, TypeError):
        return None

    employees_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "profile_picture": filename,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    return employees_collection.find_one(
        {"_id": object_id}
    )


def soft_delete_employee(
    employee_id: str,
) -> Optional[dict]:

    try:
        object_id = ObjectId(employee_id)
    except (InvalidId, TypeError):
        return None

    employees_collection.update_one(
        {"_id": object_id},
        {
            "$set": {
                "is_active": False,
                "updated_at": datetime.now(timezone.utc),
            }
        },
    )

    return employees_collection.find_one(
        {"_id": object_id}
    )


def list_employees(
    name: Optional[str] = None,
    department: Optional[str] = None,
    designation: Optional[str] = None,
    min_salary: Optional[float] = None,
    max_salary: Optional[float] = None,
    is_active: Optional[bool] = None,
    joining_year: Optional[int] = None,
    sort_by: Optional[str] = None,
    sort_order: str = "asc",
    page: int = 1,
    limit: int = 10,
) -> tuple[int, list]:

    query = {}

    if name:
        query["$or"] = [
            {
                "first_name": {
                    "$regex": name,
                    "$options": "i",
                }
            },
            {
                "second_name": {
                    "$regex": name,
                    "$options": "i",
                }
            },
        ]

    if department:
        query["department"] = {
            "$regex": f"^{department}$",
            "$options": "i",
        }

    if designation:
        query["designation"] = {
            "$regex": f"^{designation}$",
            "$options": "i",
        }

    salary_filter = {}

    if min_salary is not None:
        salary_filter["$gte"] = min_salary

    if max_salary is not None:
        salary_filter["$lte"] = max_salary

    if salary_filter:
        query["salary"] = salary_filter

    if is_active is not None:
        query["is_active"] = is_active

    if joining_year is not None:
        start_date = datetime(
            joining_year,
            1,
            1,
        )

        end_date = datetime(
            joining_year + 1,
            1,
            1,
        )

        query["joining_date"] = {
            "$gte": start_date,
            "$lt": end_date,
        }

    total_count = employees_collection.count_documents(
        query
    )

    cursor = employees_collection.find(query)

    if sort_by in ALLOWED_SORT_FIELDS:
        direction = (
            1
            if sort_order.lower() == "asc"
            else -1
        )

        cursor = cursor.sort(
            sort_by,
            direction,
        )
    else:
        cursor = cursor.sort(
            "created_at",
            -1,
        )

    skip = (page - 1) * limit

    cursor = cursor.skip(skip).limit(limit)

    return total_count, list(cursor)