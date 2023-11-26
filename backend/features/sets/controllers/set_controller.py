from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.set_schema import SetCreate, SetResponse, SetSchema, SetUpdateSchema
from features.authorization.services.token_service import TokenService, UserData
from ..services.set_service import SetService

router = APIRouter()


@router.post("/api/sets", tags=["Set"], response_model=SetResponse)
def create_set(
        set_data: SetCreate,
        db: Session = Depends(get_db),
        user_data: UserData = Depends(TokenService.get_user_data),
):
    set_service = SetService(db)
    current_user_id = user_data.id
    set = set_service.create_set_with_permission_check(set_data, current_user_id)
    return SetResponse(
        id_group=set.id_group,
        name=set.name,
        description=set.description,
        type=set.type,
        package_size=set.package_size,
        id=set.id,
    )


@router.get("/api/sets/group/{group_id}", tags=["Set"], response_model=List[SetSchema])
def get_group_sets(group_id: int, db: Session = Depends(get_db)):
    set_service = SetService(db)
    sets = set_service.get_set_by_group(group_id)
    return sets


@router.get("/api/sets/{set_id}", tags=["Set"], response_model=SetResponse)
def get_set(set_id: int, db: Session = Depends(get_db)):
    set_service = SetService(db)
    get_set = set_service.get_set_by_id(set_id)
    return SetResponse(
        id_group=get_set.id_group,
        name=get_set.name,
        description=get_set.description,
        type=get_set.type,
        package_size=get_set.package_size,
        id=get_set.id,
    )


@router.put("/api/sets/{set_id}", tags=["Set"], response_model=SetResponse)
async def update_set(
        set_id: int,
        set_update: SetUpdateSchema,
        db: Session = Depends(get_db),
):
    set_service = SetService(db)
    updated_set = set_service.update_set(
        set_id,
        set_update.id_group,
        set_update.name,
        set_update.description,
        set_update.type,
        set_update.package_size,
    )
    return SetResponse(
        id_group=updated_set.id_group,
        name=updated_set.name,
        description=updated_set.description,
        type=updated_set.type,
        package_size=updated_set.package_size,
        id=updated_set.id,
    )


@router.delete("/api/sets/{set_id}", tags=["Set"], response_model=SetResponse)
async def delete_set(
        set_id: int,
        db: Session = Depends(get_db),
):
    set_service = SetService(db)
    deleted_set = set_service.delete_set(set_id)
    return SetResponse(
        id_group=deleted_set.id_group,
        name=deleted_set.name,
        description=deleted_set.description,
        type=deleted_set.type,
        package_size=deleted_set.package_size,
        id=deleted_set.id,
    )
