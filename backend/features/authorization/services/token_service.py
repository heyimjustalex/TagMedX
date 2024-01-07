import os
from pydantic import BaseModel
from datetime import datetime, timedelta
from jose import jwt, JWTError
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, status, Request

SECRET_KEY = os.getenv(
    "AUTH_SECRET_KEY",
    "74caa9bf0fa881601db5ea5dfd2db14fd0dbd8908e40118a3a6beba43f75900d",
)
ALGORITHM = "HS256"
DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login/")


class UserData(BaseModel):
    id: int
    email: str


class TokenService:
    @staticmethod
    def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=DEFAULT_ACCESS_TOKEN_EXPIRE_MINUTES
            )
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def get_user_data(request: Request) -> UserData:
        token = request.cookies.get("token")

        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

        if not token:
            raise credentials_exception

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id = payload.get("id")
            email = payload.get("sub")
            if id is None or email is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        return UserData(id=id, email=email)
