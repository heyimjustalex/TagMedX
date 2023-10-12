from pydantic import BaseModel
from typing import List

#pydantic models for response in controllers
    
class UserResponse(BaseModel):
    user_id: int
    name: str
    password_hash: str

class UserListResponse(BaseModel):
    users: List[UserResponse]    

class ErrorResponse(BaseModel):
    message: str
