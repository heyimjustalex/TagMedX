from pydantic import BaseModel


class SetCreate(BaseModel):
    id_group: int
    package_size: int
    name: str | None = None
    description: str | None = None
    type: str | None = None


class SetResponse(BaseModel):
    id: int
    id_group: int
    package_size: int
    name: str | None = None
    description: str | None = None
    type: str | None = None


class SetUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
    type: str | None = None


class SetDeleteResponse(BaseModel):
    message: str
