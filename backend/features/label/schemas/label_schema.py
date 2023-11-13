from pydantic import BaseModel


class LabelSchema(BaseModel):
    id_set: int
    name: str
    description: str


class LabelResponse(BaseModel):
    id: int
    id_set: int
    name: str
    description: str