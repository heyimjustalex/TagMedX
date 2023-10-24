from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from features.exceptions.definitions.definitions import *
from ..services.user_service import UserService
from connectionDB.session import get_db
from typing import Annotated
from ..schemas.user_schema import (
    UserResponse,
    ErrorResponse,
    UserListResponse,
    UserCreate,
    RegisterResponse,
)

router = APIRouter()


@router.get("/api/users/", response_model=UserListResponse)
async def read_users(db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    users = user_service.get_users()

    user_responses = [
        UserResponse(user_id=user.id, name=user.name, password_hash=user.password_hash)
        for user in users
    ]

    if user_responses:
        return UserListResponse(users=user_responses)
    else:
        # here we should probably return empty list but not sure how
        # i dont think there is need for exception, but if there is
        # do it inside user_service
        return [ErrorResponse(message="Users not found")]


@router.get("/api/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    # exception handling moved to service (so there is no if in controller)
    user = user_service.get_user(user_id)
    return UserResponse(
        user_id=user.id, name=user.name, password_hash=user.password_hash
    )


@router.post("/api/register/", response_model=RegisterResponse)
async def register_user(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    user_service.register_user(
        email=new_user.email,
        password=new_user.password,
        name=new_user.name,
        surname=new_user.surname,
    )
    return RegisterResponse(message="User created successfully.")
