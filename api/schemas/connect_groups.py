from typing import Optional
from pydantic import BaseModel
from datetime import datetime, time, date
from uuid import UUID

class ConnectGroupBase(BaseModel):
    name: str
    description: Optional[str] = ""
    meeting_day: str
    meeting_time: time

class ConnectGroupCreate(ConnectGroupBase):
    pass

class ConnectGroupUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    meeting_day: Optional[str] = None
    meeting_time: Optional[time] = None

class ConnectGroupOut(ConnectGroupBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class ConnectGroupMemberBase(BaseModel):
    connect_group_id: int
    member_id: UUID
    joined_at: date
    left_at: Optional[date] = None

class ConnectGroupMemberCreate(ConnectGroupMemberBase):
    pass

class ConnectGroupMemberOut(ConnectGroupMemberBase):
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

class ConnectGroupPastorBase(BaseModel):
    connect_group_id: int
    pastor_id: int
    start_date: date
    end_date: Optional[date] = None

class ConnectGroupPastorCreate(ConnectGroupPastorBase):
    pass

class ConnectGroupPastorOut(ConnectGroupPastorBase):
    id: int
    pastor_name: Optional[str] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        if hasattr(obj, "pastor") and obj.pastor:
            data.pastor_name = f"{obj.pastor.first_name} {obj.pastor.last_name}"
        return data
