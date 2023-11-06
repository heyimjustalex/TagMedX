from typing import List

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


class TaskSchema(BaseModel):
    max_samples_for_user: int
    name: str
    description: str
    type: str


class TaskUpdateSchema(BaseModel):
    max_samples_for_user: int = None
    name: str = None
    description: str = None
    type: str = None
