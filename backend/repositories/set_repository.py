from sqlalchemy.orm import Session
from models.models import Set


class SetRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_set(self, set: Set):
        self.db.add(set)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_set(self, set: Set):
        self.db.delete(set)
        self.db.commit()

    def get_set_by_id(self, id_set: int) -> Set | None:
        return self.db.query(Set).filter(Set.id == id_set).first()

    def get_sets_by_group(self, id_group: int) -> list[Set]:
        return self.db.query(Set).filter(Set.id_group == id_group).all()

    def get_sets_by_type(self, type: str) -> list[Set]:
        return self.db.query(Set).filter(Set.type == type).all()
