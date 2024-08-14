"""
Schemas for the winners_app app
"""
from pydantic import BaseModel, Field, EmailStr


class AdminUser(BaseModel):
    """
    Base schema for the AdminUser model.
    """
    id: int = Field(..., gt=0)
    name: str = Field(..., min_length=1)
    email: EmailStr
    is_admin: bool


class HTTPError(BaseModel):
    """
    Schema for the HTTPError model.
    """
    detail: str

