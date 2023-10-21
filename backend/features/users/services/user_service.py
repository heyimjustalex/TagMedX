from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models.models import User
from typing import List
from features.exceptions.definitions.definitions import *
from passlib.context import CryptContext
from fastapi import status

# Inside services we want to use implementiations of our own exceptions
# exceptions located in ./features/exceptions/definitions
# if we do these if's and exception raise here, we keep controllers clean

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, db: Session):
        self.repository: UserRepository = UserRepository(db)

    def get_user(self, user_id: int) -> User:
        user: User = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND, detail=""
            )
        return user

    def get_users(self) -> List[User]:
        # zwroc se pusta liste
        return self.repository.get_all_users()

    def check_user(self, user_email: str, password: str) -> User:
        user: User = self.repository.get_user_by_email(user_email)
        if not user:
            raise UserNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND, detail=""
            )

        if not verify_password(password, user.password_hash):
            raise UserNotFoundException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail=""
            )

        return user

    def register_user(
        self,
        email: str,
        password: str,
        name: str | None = None,
        surname: str | None = None,
        title: str | None = None,
        role: str | None = None,
        desc: str | None = None,
        exp: str | None = None,
    ):
        user = User()
        user.e_mail = email
        user.password_hash = get_password_hash(password)
        user.name = name
        user.surname = surname
        user.title = title
        user.role = role
        user.description = desc
        user.experience = exp

        self.repository.create_user(user)
