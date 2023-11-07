from pydantic import BaseModel


class LabelSchema(BaseModel):
    name: str
    description: str
    id_set: int


class LabelResponse(BaseModel):
    id: int
    name: str
    description: str
    id_set: int
