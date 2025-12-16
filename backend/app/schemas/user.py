from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from app.schemas.signature import DeviceMetadata, GeoLocation


class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str

    organization_name: Optional[str] = None
    designation: Optional[str] = None
    phone_number: Optional[str] = None

    device_info: DeviceMetadata
    location: GeoLocation


class UserResponse(BaseModel):
    id: str
    full_name: str
    email: EmailStr
    is_active: bool