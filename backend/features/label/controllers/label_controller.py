from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from connectionDB.session import get_db
from ..schemas.label_schema import LabelSchema, LabelResponse
from ..services.label_service import LabelService
from features.authorization.services.token_service import TokenService, UserData

router = APIRouter()


@router.post("/api/labels/", tags=["Label"], response_model=LabelResponse)
def create_label(label_data: LabelSchema, db: Session = Depends(get_db),
                 user_data: UserData = Depends(TokenService.get_user_data)):
    label_service = LabelService(db)
    user_id = user_data.id
    label = label_service.create_label(user_id, label_data)
    return label


@router.get("/labels/{set_id}", tags=["Label"], response_model=List[LabelSchema])
def get_labels_for_set(
        set_id: int,
        db: Session = Depends(get_db)
):
    label_service = LabelService(db)
    labels = label_service.get_labels_for_set(set_id)
    return labels
