from typing import List
from features.exceptions.definitions.definitions import PermissionDenied
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..schemas.label_schema import LabelSchema
from repositories.label_repository import LabelRepository


class LabelService:
    def __init__(self, db: Session):
        self.label_repository = LabelRepository(db)

    def create_label(self, user_id: int, label_data: LabelSchema):
        label = self.label_repository.create_label(user_id, label_data)
        if label is None:
            raise PermissionDenied(status_code=403, detail="No authorization to create a label")
        return label

    def get_labels_for_set(self, set_id: int) -> List[LabelSchema]:
        labels = self.label_repository.get_labels_for_set(set_id)
        if not labels:
            raise HTTPException(status_code=404, detail="Brak etykiet dla podanego zadania")
        return labels
