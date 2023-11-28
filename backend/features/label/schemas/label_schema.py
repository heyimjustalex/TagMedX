from pydantic import BaseModel


class LabelCreate(BaseModel):
    id_set: int
    name: str | None = None
    description: str | None = None


class LabelResponse(BaseModel):
    id: int
    id_set: int
    name: str | None = None
    description: str | None = None


class LabelUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
