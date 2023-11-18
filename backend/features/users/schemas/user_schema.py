from pydantic import BaseModel

# pydantic models for response in controllers


class UserResponse(BaseModel):
    user_id: int
    e_mail: str
    name: str | None = None
    surname: str | None = None
    title: str | None = None
    specialization: str | None = None
    practice_start_year: int | None = None


class UserListResponse(BaseModel):
    users: list[UserResponse]


class RegisterResponse(BaseModel):
    message: str


class UserCreate(BaseModel):
    email: str
    password: str
    name: str | None = None
    surname: str | None = None


class UserUpdate(BaseModel):
    e_mail: str | None = None
    name: str | None = None
    surname: str | None = None
    title: str | None = None
    specialization: str | None = None
    practice_start_year: int | None = None
