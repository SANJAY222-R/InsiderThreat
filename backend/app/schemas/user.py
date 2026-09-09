from datetime import datetime

from pydantic import BaseModel, ConfigDict

__all__ = ["UserCreate", "UserUpdate", "UserResponse", "UserLogin", "Token"]


class UserCreate(BaseModel):
    username: str
    email: str | None = None
    password: str
    full_name: str | None = None
    role: str = "analyst"
    department: str | None = None


class UserUpdate(BaseModel):
    email: str | None = None
    full_name: str | None = None
    role: str | None = None
    department: str | None = None
    is_active: bool | None = None


class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    username: str
    email: str | None = None
    full_name: str | None = None
    role: str
    department: str | None = None
    is_active: bool
    created_at: datetime
    last_login: datetime | None = None


class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None
