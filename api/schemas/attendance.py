from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date

class AttendanceBase(BaseModel):
    member_id: int
    service_id: int

class AttendanceCreate(AttendanceBase):
    pass

class AttendanceOut(AttendanceBase):
    id: int
    created_at: datetime
    member_name: str
    service_date: date

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        data.service_date = obj.service.service_date
        return data
