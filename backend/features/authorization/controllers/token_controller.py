from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from ...users.services.user_service import UserService
from connectionDB.session import get_db
from models.models import User
from ..services.token_service import TokenService
from ..schemas.token_schema import TokenRsponse

ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter()


@router.post("/api/token/", response_model=TokenRsponse)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Annotated[Session, Depends(get_db)],
):
    user_service = UserService(db)
    user: User = user_service.check_user(form_data.username, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenService.create_access_token(
        data={"sub": user.e_mail}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
