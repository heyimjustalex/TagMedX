
from sqlalchemy.orm import Session
from models.models import User
from typing import List
class UserRepository:
    def __init__(self, db: Session):
        self.db :Session = db

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()