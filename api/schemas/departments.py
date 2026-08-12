from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class DirectorateBase(BaseModel):
    name: str
    description: Optional[str] = ""
    director_id: Optional[UUID] = None

class DirectorateCreate(DirectorateBase):
    pass

class DirectorateOut(DirectorateBase):
    id: int
    created_at: datetime
    director_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if obj.director:
            data.director_name = f"{obj.director.first_name} {obj.director.last_name}"
        return data

class DepartmentBase(BaseModel):
    name: str
    description: Optional[str] = ""
    directorate_id: int
    hod_id: Optional[UUID] = None
    assistant_hod_id: Optional[UUID] = None

class DepartmentCreate(DepartmentBase):
    pass

class DepartmentOut(DepartmentBase):
    id: int
    created_at: datetime
    directorate_name: str
    hod_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.directorate_name = obj.directorate.name
        if obj.hod:
            data.hod_name = f"{obj.hod.first_name} {obj.hod.last_name}"
        return data

class UnitBase(BaseModel):
    name: str
    description: Optional[str] = ""
    department_id: int
    unit_head_id: Optional[UUID] = None

class UnitCreate(UnitBase):
    pass

class UnitOut(UnitBase):
    id: int
    created_at: datetime
    department_name: str
    unit_head_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.department_name = obj.department.name
        if obj.unit_head:
            data.unit_head_name = f"{obj.unit_head.first_name} {obj.unit_head.last_name}"
        return data

class DepartmentMembershipBase(BaseModel):
    member_id: UUID
    department_id: int
    joined_at: date
    is_active: bool = True

class DepartmentMembershipCreate(DepartmentMembershipBase):
    pass

class DepartmentMembershipOut(DepartmentMembershipBase):
    id: int
    member_name: str
    department_name: str
    directorate_name: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        data.department_name = obj.department.name
        data.directorate_name = obj.department.directorate.name
        return data

class UnitMembershipBase(BaseModel):
    member_id: UUID
    unit_id: int
    joined_at: date
    is_active: bool = True
    role: Optional[str] = ""

class UnitMembershipCreate(UnitMembershipBase):
    pass

class UnitMembershipOut(UnitMembershipBase):
    id: int
    member_name: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        return data
