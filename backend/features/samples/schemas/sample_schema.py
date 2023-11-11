from pydantic import BaseModel


class SampleResponse(BaseModel):
    id: int
    id_package: int
    id_user: int | None = None
