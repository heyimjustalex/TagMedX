from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models.models import User
from typing import List

class UserService:
    def __init__(self, db: Session):
        self.repository : UserRepository = UserRepository(db)

    def get_user(self, user_id: int) -> User:
        return self.repository.get_user_by_id(user_id)
    
    def get_users(self) -> List[User]:
        return self.repository.get_all_users()
        