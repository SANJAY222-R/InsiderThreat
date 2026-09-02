"""
User Pydantic Schemas
=====================

Request/response models for user endpoints.
Phase 0: Schema stubs.
"""

from pydantic import BaseModel, EmailStr

__all__ = ["UserCreate", "UserUpdate", "UserResponse", "UserLogin"]


class UserCreate(BaseModel):
    """Schema for creating a new user."""
    username: str
    email: str  # TODO: Use EmailStr with email-validator installed
    password: str
    role: str = "viewer"


class UserUpdate(BaseModel):
    """Schema for updating user details."""
    email: str | None = None
    role: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    """Schema for user API responses."""
    id: int
    username: str
    email: str
    role: str
    is_active: bool


class UserLogin(BaseModel):
    """Schema for login request."""
    username: str
    password: str
