import re
from sqlalchemy.orm import Session
from repositories.user_repository import UserRepository
from models.models import User
from typing import List
from features.exceptions.definitions.definitions import *
from passlib.context import CryptContext
from fastapi import status, HTTPException

# Inside services we want to use implementiations of our own exceptions
# exceptions located in ./features/exceptions/definitions
# if we do these if's and exception raise here, we keep controllers clean

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

email_regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def valid_email(email) -> bool:
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False


def get_password_hash(password) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


class UserService:
    def __init__(self, db: Session):
        self.repository: UserRepository = UserRepository(db)

    def get_user(self, user_id: int) -> User:
        user = self.repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND, detail=""
            )
        return user

    def get_users(self) -> List[User]:
        # zwroc se pusta liste
        return self.repository.get_all_users()

    def check_user(self, email: str, password: str) -> User:
        if not valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect e-mail."
            )

        user = self.repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND, detail=""
            )

        if not verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect password."
            )

        return user

    def register_user(
        self,
        email: str,
        password: str,
        name: str | None = None,
        surname: str | None = None,
    ):
        if not valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect e-mail."
            )

        user = self.repository.get_user_by_email(email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="The user with the specified e-mail already exists.",
            )

        if name:
            name = name.capitalize()

        if surname:
            surname = surname.capitalize()

        user = User()
        user.e_mail = email
        user.password_hash = get_password_hash(password)
        user.name = name
        user.surname = surname

        self.repository.create_user(user)
