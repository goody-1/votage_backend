from typing import Optional, List
from pydantic import BaseModel
from datetime import date

class ServiceTypeBase(BaseModel):
    name: str
    description: Optional[str] = ""
    is_recurring: bool = False

class ServiceTypeCreate(ServiceTypeBase):
    pass

class ServiceTypeOut(ServiceTypeBase):
    id: int

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    service_type_id: int
    service_date: date
    theme: str
    location: str
    connect_group_id: Optional[int] = None

class ServiceCreate(ServiceBase):
    pass

class ServiceUpdate(BaseModel):
    service_type_id: Optional[int] = None
    service_date: Optional[date] = None
    theme: Optional[str] = None
    location: Optional[str] = None
    connect_group_id: Optional[int] = None

class ServiceOut(ServiceBase):
    id: int
    service_type_name: str

    class Config:
        from_attributes = True

    @classmethod
    def from_orm(cls, obj):
        data = super().from_orm(obj)
        data.service_type_name = obj.service_type.name
        return data
