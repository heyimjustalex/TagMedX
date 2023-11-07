from typing import List

from pydantic import BaseModel


class SetCreate(BaseModel):
    id_group: int
    max_samples_for_user: int
    name: str
    description: str
    type: str


class SetResponse(BaseModel):
    id: int
    id_group: int
    max_samples_for_user: int
    name: str
    description: str
    type: str


class SetSchema(BaseModel):
    # max_samples_for_user: int
    name: str
    description: str
    type: str


class SetUpdateSchema(BaseModel):
    # max_samples_for_user: int = None
    name: str = None
    description: str = None
    type: str = None
