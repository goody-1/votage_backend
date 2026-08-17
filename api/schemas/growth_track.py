from typing import Optional
from pydantic import BaseModel
from datetime import datetime, date
from uuid import UUID

class GrowthTrackBase(BaseModel):
    cohort_name: str
    start_date: date
    end_date: date
    status: str

class GrowthTrackCreate(GrowthTrackBase):
    pass

class GrowthTrackUpdate(BaseModel):
    cohort_name: Optional[str] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    status: Optional[str] = None

class GrowthTrackOut(GrowthTrackBase):
    id: int
    created_at: datetime
    enrollment_count: Optional[int] = 0

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "growthtrackenrollment_set"):
            data.enrollment_count = obj.growthtrackenrollment_set.count()
        return data

class GrowthTrackEnrollmentBase(BaseModel):
    growth_track_id: int
    member_id: UUID
    enrollment_date: date
    status: str
    graduation_date: Optional[date] = None

class GrowthTrackEnrollmentCreate(GrowthTrackEnrollmentBase):
    pass

class GrowthTrackEnrollmentOut(GrowthTrackEnrollmentBase):
    id: int
    member_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "member") and obj.member:
            data.member_name = f"{obj.member.first_name} {obj.member.last_name}"
        return data
