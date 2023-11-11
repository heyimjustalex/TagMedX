from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.set_schema import SetCreate, SetResponse, SetSchema, SetUpdateSchema
from features.authorization.services.token_service import TokenService, UserData
from ..services.set_service import SetService

router = APIRouter()


@router.post("/api/sets/create", tags=["Set"], response_model=SetResponse)
def create_set(
        set_data: SetCreate,
        db: Session = Depends(get_db),
        user_data: UserData = Depends(TokenService.get_user_data),
):
    set_service = SetService(db)
    current_user_id = user_data.id
    set = set_service.create_set_with_permission_check(set_data, current_user_id)
    return set


@router.get("/api/sets", tags=["Set"], response_model=List[SetSchema])
def get_sets(db: Session = Depends(get_db), user_data: UserData = Depends(TokenService.get_user_data)):
    set_service = SetService(db)
    user_id = user_data.id
    sets = set_service.get_user_sets(user_id)
    return sets


@router.get("/api/sets/{set_id}", tags=["Set"], response_model=SetResponse)
def get_set(set_id: int, db: Session = Depends(get_db)):
    set_service = SetService(db)
    set = set_service.get_set_by_id(set_id)
    return set


@router.put("/update_set/{set_id}", tags=["Set"], response_model=SetResponse)
async def update_set(
        set_id: int,
        set_data: SetUpdateSchema,
        db: Session = Depends(get_db),
):
    set_service = SetService(db)
    set = set_service.update_set(set_id, set_data.dict())
    return set


@router.delete("/delete_set/{set_id}", tags=["Set"], response_model=SetResponse)
async def delete_set(
        set_id: int,
        db: Session = Depends(get_db),
):
    set_service = SetService(db)
    set = set_service.delete_set(set_id)
    return set
