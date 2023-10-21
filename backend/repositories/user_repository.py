from sqlalchemy.orm import Session
from models.models import User
from typing import List

# Repository that talks to database through db session object with SQLAlchemy


class UserRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def get_user_by_id(self, user_id: int) -> User:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return self.db.query(User).filter(User.e_mail == email).first()

    def get_all_users(self) -> List[User]:
        return self.db.query(User).all()

    def create_user(self, user: User):
        self.db.add(user)
        self.db.commit()
