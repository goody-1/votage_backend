from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from apps.departments.models import Directorate, Department, Unit, DepartmentMembership, UnitMembership
from ..schemas.departments import (
    DirectorateCreate, DirectorateOut,
    DepartmentCreate, DepartmentOut,
    UnitCreate, UnitOut,
    DepartmentMembershipCreate, DepartmentMembershipOut,
    UnitMembershipCreate, UnitMembershipOut
)
from ..deps import get_current_admin_user

router = APIRouter(
    prefix="/departments",
    tags=["Departments"],
    dependencies=[Depends(get_current_admin_user)]
)

# Directorates
@router.get("/directorates/", response_model=List[DirectorateOut])
def list_directorates():
    return [DirectorateOut.from_orm(d) for d in Directorate.objects.all()]

@router.post("/directorates/", response_model=DirectorateOut)
def create_directorate(d_in: DirectorateCreate):
    d = Directorate.objects.create(**d_in.dict())
    return DirectorateOut.from_orm(d)

# Departments
@router.get("/", response_model=List[DepartmentOut])
def list_departments():
    return [DepartmentOut.from_orm(d) for d in Department.objects.all().select_related("directorate", "hod")]

@router.post("/", response_model=DepartmentOut)
def create_department(d_in: DepartmentCreate):
    d = Department.objects.create(**d_in.dict())
    return DepartmentOut.from_orm(d)

# Units
@router.get("/units/", response_model=List[UnitOut])
def list_units():
    return [UnitOut.from_orm(u) for u in Unit.objects.all().select_related("department", "unit_head")]

@router.post("/units/", response_model=UnitOut)
def create_unit(u_in: UnitCreate):
    u = Unit.objects.create(**u_in.dict())
    return UnitOut.from_orm(u)

from uuid import UUID

# Memberships
@router.get("/memberships/", response_model=List[DepartmentMembershipOut])
def list_dept_memberships(
    member_id: Optional[UUID] = None,
    department_id: Optional[int] = None
):
    queryset = DepartmentMembership.objects.all().select_related("member", "department", "department__directorate")
    if member_id:
        queryset = queryset.filter(member_id=member_id)
    if department_id:
        queryset = queryset.filter(department_id=department_id)
    return [DepartmentMembershipOut.from_orm(m) for m in queryset]

@router.post("/memberships/", response_model=DepartmentMembershipOut)
def join_department(m_in: DepartmentMembershipCreate):
    m = DepartmentMembership.objects.create(**m_in.dict())
    return DepartmentMembershipOut.from_orm(m)
