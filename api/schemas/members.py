from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from datetime import date, datetime

from uuid import UUID

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
    department_name: Optional[str] = "Regular member"

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        return cls(
            id=obj.id,
            first_name=obj.first_name,
            last_name=obj.last_name,
            full_name=f"{obj.first_name} {obj.last_name}",
            phone_number=obj.phone_number,
            email=obj.email,
            gender=obj.gender,
            date_joined=obj.date_joined,
            department_name=cls.get_department(obj)
        )

    @staticmethod
    def get_department(obj):
        try:
            from apps.departments.models import DepartmentMembership
            membership = DepartmentMembership.objects.filter(member=obj, is_active=True).first()
            if membership:
                return membership.department.name
        except Exception:
            pass
        return "Regular member"

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
