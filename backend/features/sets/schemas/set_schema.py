from typing import List
from pydantic import BaseModel


class SetCreate(BaseModel):
    id_group: int
    name: str
    description: str
    type: str
    package_size: int


class SetResponse(BaseModel):
    id: int
    id_group: int
    name: str
    description: str
    type: str
    package_size: int


class SetSchema(BaseModel):
    id: int
    name: str
    description: str
    type: str
    package_size: int


class SetUpdateSchema(BaseModel):
    id_group: int | None = None
    name: str | None = None
    description: str | None = None
    type: str | None = None
    package_size: int | None = None
