from typing import Optional
from pydantic import BaseModel, EmailStr

class PastorBase(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: EmailStr

class PastorCreate(PastorBase):
    pass

class PastorUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None

class PastorOut(PastorBase):
    id: int

    class Config:
        from_attributes = True
