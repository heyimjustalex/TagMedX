from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.label_repository import LabelRepository
from models.models import Label


class LabelService:
    def __init__(self, db: Session):
        self.repository = LabelRepository(db)

    def create_label(
        self,
        id_set: int,
        name: str | None = None,
        desc: str | None = None,
        color: str | None = None,
    ) -> Label:
        label = Label()
        label.id_set = id_set
        label.name = name
        label.description = desc
        label.color = color

        self.repository.create_label(label)
        return label

    def update_label(
        self,
        id_label: int,
        name: str | None = None,
        description: str | None = None,
        color: str | None = None,
    ) -> Label:
        label = self.get_label(id_label)

        if name:
            label.name = name

        if description:
            label.description = description

        label.color = color

        self.repository.update()
        return label

    def delete_label(self, id_label: int):
        label = self.get_label(id_label)
        self.repository.delete_label(label)

    def get_label(self, id_label: int) -> Label:
        label = self.repository.get_label_by_id(id_label)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Label not found"
            )
        return label

    def get_labels_for_set(self, id_set: int) -> list[Label]:
        return self.repository.get_labels_by_set(id_set)

    def get_labels_in_group(self, id_group: int) -> list[Label]:
        return self.repository.get_labels_by_group(id_group)

    def check_if_label_exists_and_belongs_to_set(self, id_label: int, id_set: int):
        label = self.get_label(id_label)
        if label.id_set != id_set:
            raise HTTPException(
                status_code=status.HTTP_406_NOT_ACCEPTABLE,
                detail=f"Label {id_label} does not belong to the set",
            )
