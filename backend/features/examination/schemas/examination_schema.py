from pydantic import BaseModel
from ...bbox.schemas.bbox_schema import ExtendedBBoxResponse


class ExaminationResponse(BaseModel):
    id: int
    user: str
    role: str
    id_user: int
    id_sample: int
    tentative: bool


class ExtendedExaminationResponse(ExaminationResponse):
    bboxes: list[ExtendedBBoxResponse]


class BBoxCreate(BaseModel):
    id_label: int
    comment: str | None = None
    x: int | None = None
    y: int | None = None
    width: int | None = None
    height: int | None = None


class ExaminationCreate(BaseModel):
    id_sample: int
    BBox: list[BBoxCreate]
    tentative: bool = False
