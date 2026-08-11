from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

from uuid import UUID

class MemberDepartmentOut(BaseModel):
    id: int
    name: str
    directorate_id: int
    directorate_name: str
    joined_at: Optional[date] = None
    is_active: bool = True

    class Config:
        from_attributes = True

class MemberBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    date_joined: Optional[datetime] = None

class MemberCreate(MemberBase):
    pass

class MemberUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    gender: Optional[str] = None
    date_joined: Optional[datetime] = None

class MemberOut(MemberBase):
    id: UUID
    full_name: Optional[str] = None
    is_worker: bool = False
    departments: List[MemberDepartmentOut] = []
    department_name: Optional[str] = "Regular member"

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        deps = cls.get_departments(obj)
        is_worker = len(deps) > 0
        dept_name_str = ", ".join([d.name for d in deps]) if deps else "Regular member"

        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            full_name=f"{obj.first_name} {obj.last_name}",
            phone_number=obj.phone_number,
            email=obj.email,
            gender=obj.gender,
            date_joined=obj.date_joined,
            is_worker=is_worker,
            departments=deps,
            department_name=dept_name_str
        )

    @staticmethod
    def get_departments(obj):
        try:
            from apps.departments.models import DepartmentMembership
            memberships = DepartmentMembership.objects.filter(
                member=obj, is_active=True
            ).select_related("department", "department__directorate")
            
            res = []
            for m in memberships:
                res.append(MemberDepartmentOut(
                    id=m.department.id,
                    name=m.department.name,
                    directorate_id=m.department.directorate.id,
                    directorate_name=m.department.directorate.name,
                    joined_at=m.joined_at,
                    is_active=m.is_active
                ))
            return res
        except Exception:
            return []

class FirstTimerBase(BaseModel):
    member_id: int
    service_id: Optional[int] = None
    service_name: str
    service_date: date

class FirstTimerCreate(FirstTimerBase):
    pass

class FirstTimerOut(FirstTimerBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
