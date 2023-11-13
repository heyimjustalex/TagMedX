from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ...users.services.user_service import UserService
from connectionDB.session import get_db
from ..services.token_service import TokenService
from ..schemas.token_schema import TokenCreate
from ...users.schemas.user_schema import UserResponse

ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


@router.post("/api/login/", tags=["Authorization"], response_model=UserResponse)
async def login(
    form_data: TokenCreate, db: Annotated[Session, Depends(get_db)], response: Response
):
    user_service = UserService(db)
    user = user_service.check_user(form_data.email, form_data.password)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = TokenService.create_access_token(
        data={"id": user.id, "sub": user.e_mail}, expires_delta=access_token_expires
    )

    user_data = UserResponse(
        user_id=user.id,
        e_mail=user.e_mail,
        name=user.name,
        surname=user.surname,
        title=user.title,
        specialization=user.specialization,
        practice_start_year=user.practice_start_year,
    )

    response.set_cookie(
        key="token",
        value=access_token,
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        secure=True,
        samesite="none",
    )

    return user_data
