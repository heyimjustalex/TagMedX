from sqlalchemy.orm import Session
from models.models import Label, Set


class LabelRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_label(self, label: Label):
        self.db.add(label)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_label(self, label: Label):
        self.db.delete(label)
        self.db.commit()

    def get_label_by_id(self, id_label: int) -> Label | None:
        return self.db.query(Label).filter(Label.id == id_label).first()

    def get_labels_by_set(self, id_set: int) -> list[Label]:
        return self.db.query(Label).filter(Label.id_set == id_set).all()

    def get_labels_by_group(self, id_group: int) -> list[Label]:
        return (
            self.db.query(Label).filter(Label.Set.has(Set.id_group == id_group)).all()
        )
