from sqlalchemy.orm import Session
from models.models import BBox


class BBoxRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bbox(self, bbox: BBox):
        self.db.add(bbox)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_bbox(self, bbox: BBox):
        self.db.delete(bbox)
        self.db.commit()

    def get_bbox_by_id(self, id_bbox: int) -> BBox | None:
        return self.db.query(BBox).filter(BBox.id == id_bbox).first()

    def get_bboxes_by_examination(self, id_examination: int) -> list[BBox]:
        return self.db.query(BBox).filter(BBox.id_examination == id_examination).all()

    def get_bboxes_by_label(self, id_label: int) -> list[BBox]:
        return self.db.query(BBox).filter(BBox.id_label == id_label).all()

    def delete_bboxes_by_examination(self, id_examination: int):
        self.db.query(BBox).filter(BBox.id_examination == id_examination).delete()
        self.db.commit()
