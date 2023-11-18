from pydantic import BaseModel


class SampleResponse(BaseModel):
    id: int
    id_package: int


class SampleListResponse(BaseModel):
    samples: list[SampleResponse]
