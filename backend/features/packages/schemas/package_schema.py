from pydantic import BaseModel


class PackageResponse(BaseModel):
    id: int
    id_set: int
    id_user: int | None = None
    is_ready: bool | None = None
