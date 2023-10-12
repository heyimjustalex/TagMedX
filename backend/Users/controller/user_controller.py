from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..schema.user_schema import UserResponse, ErrorResponse, UserListResponse
from ..service.user_service import UserService
from utility.session import get_db

router = APIRouter()




@router.get("/users/", response_model=UserListResponse)
async def read_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    users = user_service.get_users()

    user_responses = [UserResponse(user_id=user.id, name=user.name, password_hash=user.password_hash) for user in users]

    if user_responses:
        return UserListResponse(users=user_responses)
    else:
        return ErrorResponse(message="Users not found")

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    user = user_service.get_user(user_id)

    if user:
        return UserResponse(user_id=user.id, name=user.name, password_hash=user.password_hash)
    else:
        return ErrorResponse(message="User not found")
