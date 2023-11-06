from pydantic import BaseModel


class SampleResponse(BaseModel):
    id: int
    id_task: int
    id_user: int | None = None
