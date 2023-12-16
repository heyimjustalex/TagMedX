from pydantic import BaseModel
from ...label.schemas.label_schema import LabelResponse



class BBoxCreate(BaseModel):
    id_examination: int
    id_label: int
    comment: str | None = None
    x: int | None = None
    y: int | None = None
    width: int | None = None
    height: int | None = None


class BBoxResponse(BaseModel):
    id: int
    id_examination: int
    id_label: int
    comment: str | None = None
    x: int | None = None
    y: int | None = None
    width: int | None = None
    height: int | None = None


class ExtendedBBoxResponse(BBoxResponse):
    label: LabelResponse


class BBoxUpdate(BaseModel):
    comment: str | None = None
    x: int | None = None
    y: int | None = None
    width: int | None = None
    height: int | None = None
