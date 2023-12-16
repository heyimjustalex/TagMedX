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
        id_bbox: int,
        comment: str | None = None,
        x: int | None = None,
        y: int | None = None,
        width: int | None = None,
        height: int | None = None,
    ) -> BBox:
        bbox = self.get_bbox_by_id(id_bbox)
        if not bbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="BBox not found"
            )

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

        self.repository.update_bbox()
        return bbox

    def delete_bbox(self, id_bbox: int):
        bbox = self.get_bbox_by_id(id_bbox)
        if not bbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="BBox not found"
            )
        self.repository.delete_bbox(bbox)

    def get_bbox_by_id(self, id_bbox: int) -> BBox:
        bbox = self.repository.get_bbox_by_id(id_bbox)
        if not bbox:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="BBox not found"
            )
        return bbox

    def get_bbox_by_examination(self, id_examination: int) -> list[BBox]:
        examination = self.repository.get_bbox_by_examination(id_examination)
        if not examination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="BBox_by_examination not found",
            )
        return examination

    def get_bbox_by_label(self, id_label: int) -> list[BBox]:
        label = self.repository.get_bbox_by_label(id_label)
        if not label:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="BBox_by_label not found"
            )
        return label

    # def check_user_is_assigned_to_package(self, user_id: int) -> BBox:
    #     user = self.repository.check_user_is_assigned_to_package(user_id)
    #     if not user:
    #         raise HTTPException(
    #             status_code=status.HTTP_404_NOT_FOUND, detail="Permission denied"
    #         )
    #     return user
