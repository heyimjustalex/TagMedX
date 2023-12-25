from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.bbox_repository import BBoxRepository
from models.models import BBox


class BBoxService:
    def __init__(self, db: Session):
        self.repository = BBoxRepository(db)

    def create_bbox(
        self,
        id_examination: int,
        id_label: int,
        comment: str | None = None,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> BBox:
        bbox = BBox()
        bbox.id_examination = id_examination
        bbox.id_label = id_label
        bbox.comment = comment
        bbox.x = x
        bbox.y = y
        bbox.width = width
        bbox.height = height

        self.repository.create_bbox(bbox)
        return bbox

    def update_bbox(
        self,
        bbox: BBox,
        comment: str | None = None,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> BBox:
        if comment:
            bbox.comment = comment

        if x:
            bbox.x = x

        if y:
            bbox.y = y

        if width:
            bbox.width = width

        if height:
            bbox.height = height

        self.repository.update()
        return bbox

    def delete_bbox(self, bbox: BBox):
        self.repository.delete_bbox(bbox)

    def get_bbox(self, id_bbox: int) -> BBox:
        bbox = self.repository.get_bbox_by_id(id_bbox)
        if not bbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="BBox not found"
            )
        return bbox

    def get_examination_bboxes(self, id_examination: int) -> list[BBox]:
        return self.repository.get_bboxes_by_examination(id_examination)

    def get_label_bboxes(self, id_label: int) -> list[BBox]:
        return self.repository.get_bboxes_by_label(id_label)

    def delete_examination_bboxes(self, id_examination: int):
        self.repository.delete_bboxes_by_examination(id_examination)
