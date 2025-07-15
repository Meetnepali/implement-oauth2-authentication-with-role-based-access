from pydantic import BaseModel, EmailStr, validator, Field
from typing import Optional
import re

PHONE_REGEX = re.compile(r"^\+?1?\d{9,15}$")

class ProfileBase(BaseModel):
    full_name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None, description="URL to the user's avatar image")
    
    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not PHONE_REGEX.match(v):
            raise ValueError('Phone number must be valid international format (e.g. +123456789)')
        return v

class ProfileCreate(ProfileBase):
    pass

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    avatar_url: Optional[str] = Field(None)

    @validator('phone')
    def validate_phone(cls, v):
        if v is None:
            return v
        if not PHONE_REGEX.match(v):
            raise ValueError('Phone number must be valid international format (e.g. +123456789)')
        return v

class ProfileOut(ProfileBase):
    id: int

class ErrorResponse(BaseModel):
    detail: str
    code: int
