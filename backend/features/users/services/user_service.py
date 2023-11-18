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


def valid_email(email: str) -> bool:
    if re.fullmatch(email_regex, email):
        return True
    else:
        return False


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
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
        return self.repository.get_all_users()

    def get_users_in_group(self, id_group) -> List[User]:
        return self.repository.get_users_by_group(id_group)

    def get_user_by_email(self, email: str) -> User:
        user = self.repository.get_user_by_email(email)
        if not user:
            raise UserNotFoundException(
                status_code=status.HTTP_404_NOT_FOUND, detail=""
            )
        return user

    def check_user(self, email: str, password: str) -> User:
        if not valid_email(email):
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Incorrect e-mail."
            )

        user = self.get_user_by_email(email)

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

    def update_user(
        self,
        id_user: int,
        email: str | None = None,
        name: str | None = None,
        surname: str | None = None,
        title: str | None = None,
        specialization: str | None = None,
        practice_start_year: int | None = None,
    ) -> User:
        user = self.get_user(id_user)

        if email:
            if not valid_email(email):
                raise HTTPException(
                    status_code=status.HTTP_406_NOT_ACCEPTABLE,
                    detail="Incorrect e-mail.",
                )

            user_exists = self.repository.get_user_by_email(email)
            if user_exists and user_exists.id != id_user:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="The user with the specified e-mail already exists.",
                )

            user.e_mail = email

        if name:
            user.name = name.capitalize()

        if surname:
            user.surname = surname.capitalize()

        if title:
            user.title = title

        if specialization:
            user.specialization = specialization

        if practice_start_year:
            user.practice_start_year = practice_start_year

        self.repository.update()
        return user
