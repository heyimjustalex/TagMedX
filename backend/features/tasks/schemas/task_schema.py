from pydantic import BaseModel


class TaskCreate(BaseModel):
    id_group: int
    max_samples_for_user: int
    name: str
    description: str
    type: str


class TaskResponse(BaseModel):
    id: int
    id_group: int
    max_samples_for_user: int
    name: str
    description: str
    type: str
