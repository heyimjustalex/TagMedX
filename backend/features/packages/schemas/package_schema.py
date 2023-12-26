from pydantic import BaseModel
from ...samples.schemas.sample_schema import ExtendedSampleResponse


class PackageResponse(BaseModel):
    id: int
    id_set: int
    all: int
    tentative: int
    id_user: int | None = None
    is_ready: bool | None = None


class ExtendedPackageResponse(PackageResponse):
    samples: list[ExtendedSampleResponse]
