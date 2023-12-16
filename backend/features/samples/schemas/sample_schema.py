from pydantic import BaseModel
from ...examination.schemas.examination_schema import ExtendedExaminationResponse


class SampleResponse(BaseModel):
    id: int
    id_package: int


class ExtendedSampleResponse(SampleResponse):
    examinations: list[ExtendedExaminationResponse]
