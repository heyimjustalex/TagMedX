from pydantic import BaseModel
from typing import List

# pydantic models for response in controllers


class UserResponse(BaseModel):
    user_id: int
    name: str
    password_hash: str


class UserListResponse(BaseModel):
    users: List[UserResponse]


class ErrorResponse(BaseModel):
    message: str


class RegisterResponse(BaseModel):
    message: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None
    surname: str | None = None
    title: str | None = None
    description: str | None = None
    experience: str | None = None
