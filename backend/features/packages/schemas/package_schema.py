from pydantic import BaseModel
from ...samples.schemas.sample_schema import ExtendedSampleResponse


class PackageResponse(BaseModel):
    id: int
    id_set: int
    all: int
    tentative: int
    is_ready: bool
    id_user: int | None = None


class ExtendedPackageResponse(PackageResponse):
    samples: list[ExtendedSampleResponse]
