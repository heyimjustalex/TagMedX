from sqlalchemy.orm import Session
from models.models import BBox, Examination, Sample, Package


class BBoxRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_bbox(self, bbox: BBox):
        self.db.add(bbox)
        self.db.commit()

    def update_bbox(self):
        self.db.commit()

    def delete_bbox(self, bbox: BBox):
        self.db.delete(bbox)
        self.db.commit()

    def get_bbox_by_id(self, id_bbox: int) -> BBox | None:
        return self.db.query(BBox).filter(BBox.id == id_bbox).first()

    def get_bbox_by_examination(self, id_examination: int) -> list[BBox]:
        return self.db.query(BBox).filter(BBox.id_examination == id_examination).all()

    def get_bbox_by_label(self, id_label: int) -> list[BBox]:
        return self.db.query(BBox).filter(BBox.id_label == id_label).all()

    # def check_user_is_assigned_to_package(self, user_id: int) -> BBox | None:
    #     return (
    #         self.db.query(BBox)
    #         .filter(BBox.Examination.has(Examination.Sample.has(Sample.Package.has(Package.id_user == user_id))))
    #     )
