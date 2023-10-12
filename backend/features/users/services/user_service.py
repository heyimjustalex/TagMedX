from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models.models import User
from typing import List
from features.exceptions.definitions.definitions import *

# Inside services we want to use implementiations of our own exceptions
# exceptions located in ./features/exceptions/definitions
# if we do these if's and exception raise here, we keep controllers clean
    
class UserService:
    def __init__(self, db: Session):
        self.repository : UserRepository = UserRepository(db)

    def get_user(self, user_id: int) -> User:
        user : User = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(status_code=404,detail="")
        return user

    def get_users(self) -> List[User]:
        #zwroc se pusta liste
        return self.repository.get_all_users()
        