from pydantic import BaseModel


class PackageResponse(BaseModel):
    id: int
    id_set: int
    id_user: int | None
    is_ready: bool | None


class PackageListResponse(BaseModel):
    packages: list[PackageResponse]
