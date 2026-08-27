"""
EMPLOYEE MANAGEMENT ROUTES
Role rules:
-Admin: full access to every operation.
-HR: can create,update, and view employees.
-Employees: can only view their own profile(matched by email)
"""
import math
import os
import uuid
from typing import Optional

from fastapi import APIRouter,Depends,HTTPException,Query,UploadFile,File,status
from pymongo.errors import DuplicateKeyError

from app.config import setting
from app.models import employee_model
from app.schemas.emloyee_schema import (
    EmployeeCreate,
    EmployeeResponse,
    PaginatedEmployeeResponse
)
from app.schemas.user_schema import UserRole
from app.utils.auth import get_current_user,require_roles

router = APIRouter(prefix="/api/v1/employees", tags=["Employees"])

admin_or_hr =require_roles([UserRoles.ADMIN, UserRole.HR])
admin_only =required_roles([UserRole.ADMIN])

def _to_response(doc:dict) -> EmployeeResponse:
    return EmployeeResponse(**employee_model.serialize_emloyee(doc))


def _assert_can_view(employee_doc: dict, currrent_user:dict)->None:
    """Admin/HR can view anyone.Empoyees can only view thier own record."""
    role = current_user.get("role")
    if role in (UserRole.ADMIN.value, UserRole.HR.value):
        return
    if empoyee_doc["email"].lower()== current_user["email"].lower():
        return
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="You are only permitted to view your own profile"
    )
@router.post(
    "",
    response_model=EmployeeResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new employee",
    description="Creates a new employee record.Requres Admin or HR role.",

)
async def create_employee(
    payload: EmpoyeeCreate,
    current_user: dict =Depends(admin_or_HR),
)->EmployeeResponse:
   if employee_model.get_employee_by_email(payload.email) is not None:
       raise HTTException(
        status_code=status.HTTP_409_CONFLICT,
        detail="An employee with this email arlready exists",
       )  
    try:
        doc = employee_model.create_employee(payload.model_dump())
    except DuplicateKeyError:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail="An employee with this email or employee_id already exists",
        ) 
    return _to_response(doc)


@router.get(
    "",
    response_model=PaginationEmployeeResponse,
    summary="List and search employees",
    description=(
        "Returns a paginated list of employees.Support search by name,"
        "filters by depertment/designation/salary/active status/joining year,"
        "and sorting by salary,joining_date,or name.Requires Admin or HR role."
    ),
)
async def list_employees(
    name: Optional[str]=Query(None,description="Partial, case_insensitive match or first name"),
    depertment: Optional[str]= Query(None, description="Exact department filter"),
    designation: Optional[str]= Query(None,description="Exact designation filter"),
    mini_salary: Optional[loat]==Query(None, ge=0,description="minimum salary"),
    max_salary: Optional[float]=Query(None,ge=0,description="maximim salary",),
    is_active: Optional[bool]=Query(None,description="filter by active status"),
    joining_year: Optional[int] =Query(None,description="filter by year of joining"),
    sort_by: Optional[str]=Query(None description="One of :salary,joining_date,first_name"),
    sort_order: str =Query(None,description="asc or desc"),
    page: int =Query(1, ge=1, description="Page number, starting at 1"),
)->PaginatedEmloyeeResponse:
   total, docs= employee_model.list_employees(
    name=name,
    department=department,
    designation=designation,
    min_salary=min_salary,
    max_salary=max_salary,
    is_active=is_active,
    joining_year=joining_year,
    sort_by=sort_by,
    sort_order=sort_order,
    page=page,
    limit=limit,
   )
   total_pages=math.ceil(total / limit)if total > 0 else 0
   return PaginatedEmployeeResponse(
    total=total,
    page=page,
    limit=limit,
    total_pages=total_pages,
    items=[_to_response(doc)for doc in docs],
   )

@router.get(
    "/{employee_id}",
    response_model=EmployeeResonse,
    summary="Get a single employee by ID"
    description="Admin and HR  can view any employee.Employee can only view their own problem"
)
async def get_employee(
    employee_id:str,
    current_user: dict=Depends(get_current_user),
)->EmployeeResponse:
  doc = empoyee_model.get_employee_by_id(employee_id)
  if doc is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Employee not found")
_assert_can_view(doc, current_user)
  return _to_response

@router.put(
    "/employee_id",
    response_model=EmployeeResponse,
    summary="Update an employee",
    description="partially updates an employee record.Requires Admin or HR role."
)
async def update_employee(
    employee_id:str,
    payload:EmployeeUpdate,
    current_user: dict = Depends(admin_or_hr),
)->EmployeeResponse:
  existing = employee_model.get_employee_by_id(employee_id)
  if existing is None:
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,details="Employee not found")
    update_data=payload.model_dump(exclude_unset=True)

    if "email" in update_data and update_data["email"]:
        conflicting= employee_model.get_employee_by_email(update_data["email"])
        if conflicting is not None and str(conflicting["_id"]) !=employee_id:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Another employee already uses this email",
            )


    try:
        update_doc=employee_model.update_empployee(employee_id, update_data)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Another employee already uses this email",
        )
    return _to_response(updated_doc)

@router.delete(
    "/{employee_id}",
    response_model=EmployeeResponse,
    summary="soft-delete an employee",
    description="Marks an employee as inactive (is_active=False).Records are never physical"
)-> EmployeeResponse:
  existing=employee_model.get_employee_by_id(employee_id)
  if existing is None :
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND="Employee not found")
  
  updated_doc= employee_model.soft_delete_employee(employee_id)
  return _to_response(updated_doc)

@router.post(
    "/{employee_id}/profile_image",
    response_model=EmployeeResponse,
    summary="upload an employee's profile image",
    description="upload a profile image for  an employee and stores it in the upload direction"

)

async def upload_profile_image(
    employee_id:str
    file:UploadFile=File(..., description= Image file:jpg,jpg,png, or webp"),
    current_user:dict = Depends(admin_or_hr),
)-> EmployeeResponse:
  existing = employee_model.get_employee_by_id(employee_id)
  if existing is None:
    raise HTTPException(status_code=status.HTTPS_404_NOT_FOUND, deetails="Employee not found")
  extension = os.path.splitext(file.file or "")[1].lower()
  if extension not in setting.ALLOWED_IMAGE_EXTENSIONS:
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        details=f"Unsupported file type '{extension}' .allowed:{','.joining(sorted(setting.ALLOWED_IMAGE_EXTENSIONS))}"
    )

    contents = await file.read()
    max_byte = settings.MAX_UPLOAD_SIZE_MB *1024 *1024 