from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class EventBase(BaseModel):
    service_id: int
    event_type: str
    description: str

class EventCreate(EventBase):
    pass

class EventUpdate(BaseModel):
    service_id: Optional[int] = None
    event_type: Optional[str] = None
    description: Optional[str] = None

class EventOut(EventBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class EventParticipationBase(BaseModel):
    event_id: int
    member_id: Optional[int] = None
    participant_name: str
    role: str

class EventParticipationCreate(EventParticipationBase):
    pass

class EventParticipationOut(EventParticipationBase):
    id: int

    class Config:
        from_attributes = True
