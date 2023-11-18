from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from features.exceptions.definitions.definitions import *
from ..services.user_service import UserService
from connectionDB.session import get_db
from typing import Annotated
from ...authorization.services.token_service import UserData, TokenService
from ..schemas.user_schema import (
    UserResponse,
    UserListResponse,
    UserCreate,
    UserUpdate,
    RegisterResponse,
)

router = APIRouter()


@router.get("/api/users/", tags=["Users"], response_model=UserListResponse)
async def read_users(db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    users = user_service.get_users()

    response = UserListResponse(users=[])
    for user in users:
        response.users.append(
            UserResponse(
                user_id=user.id,
                e_mail=user.e_mail,
                name=user.name,
                surname=user.surname,
                title=user.title,
                specialization=user.specialization,
                practice_start_year=user.practice_start_year,
            )
        )

    return response


@router.get("/api/users/{user_id}", tags=["Users"], response_model=UserResponse)
async def read_user(user_id: int, db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    user = user_service.get_user(user_id)
    return UserResponse(
        user_id=user.id,
        e_mail=user.e_mail,
        name=user.name,
        surname=user.surname,
        title=user.title,
        specialization=user.specialization,
        practice_start_year=user.practice_start_year,
    )


@router.post("/api/register/", tags=["Authorization"], response_model=RegisterResponse)
async def register_user(new_user: UserCreate, db: Annotated[Session, Depends(get_db)]):
    user_service = UserService(db)
    user_service.register_user(
        email=new_user.email,
        password=new_user.password,
        name=new_user.name,
        surname=new_user.surname,
    )
    return RegisterResponse(message="User created successfully.")


@router.put("/api/users/update", tags=["Users"], response_model=UserResponse)
async def update_user(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    user_update: UserUpdate,
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)
    user = user_service.update_user(
        user_data.id,
        user_update.e_mail,
        user_update.name,
        user_update.surname,
        user_update.title,
        user_update.specialization,
        user_update.practice_start_year,
    )
    return UserResponse(
        user_id=user.id,
        e_mail=user.e_mail,
        name=user.name,
        surname=user.surname,
        title=user.title,
        specialization=user.specialization,
        practice_start_year=user.practice_start_year,
    )
