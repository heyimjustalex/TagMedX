from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.label_schema import LabelSchema, LabelResponse, LabelUpdate
from ..services.label_service import LabelService
from features.authorization.services.token_service import TokenService, UserData

router = APIRouter()


@router.post("/api/labels/", tags=["Label"], response_model=LabelResponse)
def create_label(label_data: LabelSchema, db: Session = Depends(get_db),
                 user_data: UserData = Depends(TokenService.get_user_data)):
    label_service = LabelService(db)
    user_id = user_data.id
    label = label_service.create_label(user_id, label_data)
    return LabelResponse(
        id=label.id,
        id_set=label.id_set,
        name=label.name,
        description=label.description,
    )


@router.get("/labels/set/{set_id}", tags=["Label"], response_model=List[LabelSchema])
def get_labels_for_set(
        set_id: int,
        db: Session = Depends(get_db)
):
    label_service = LabelService(db)
    labels = label_service.get_labels_for_set(set_id)
    return labels


@router.put("/labels/{label_id}", tags=["Label"], response_model=LabelResponse)
def update_label(
        label_id: int,
        label_update: LabelUpdate,
        db: Session = Depends(get_db)
):
    label_service = LabelService(db)
    updated_label = label_service.update_label(
        label_id,
        name=label_update.name,
        description=label_update.description,
    )
    return LabelResponse(
        id=updated_label.id,
        id_set=updated_label.id_set,
        name=updated_label.name,
        description=updated_label.description,
    )


@router.delete("/labels/{label_id}", tags=["Label"], response_model=LabelResponse)
def delete_label(
        label_id: int,
        db: Session = Depends(get_db),
):
    label_service = LabelService(db)
    deleted_group = label_service.delete_label(label_id)
    return LabelResponse(
        id=deleted_group.id,
        id_set=deleted_group.id_set,
        name=deleted_group.name,
        description=deleted_group.description,
    )
