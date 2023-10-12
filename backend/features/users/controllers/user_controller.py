from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..schemas.user_schema import UserResponse, ErrorResponse, UserListResponse
from features.exceptions.definitions.definitions import *
from ..services.user_service import UserService
from connectionDB.session import get_db

router = APIRouter()

@router.get("/users/", response_model=UserListResponse)
async def read_users(db: Session = Depends(get_db)):
    user_service = UserService(db)
    users = user_service.get_users()

    user_responses = [UserResponse(user_id=user.id, name=user.name, password_hash=user.password_hash) for user in users]

    if user_responses:
        return UserListResponse(users=user_responses)
    else:
        # here we should probably return empty list but not sure how 
        # i dont think there is need for exception, but if there is
        # do it inside user_service
        return [ErrorResponse(message="Users not found")]

@router.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user_service = UserService(db)
    #exception handling moved to service (so there is no if in controller)
    user = user_service.get_user(user_id)       
    return UserResponse(user_id=user.id, name=user.name, password_hash=user.password_hash)
 
       
