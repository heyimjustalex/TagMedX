from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..schemas.sample_schema import SampleResponse
from ..services.sample_service import SampleService


router = APIRouter()


@router.post(
    "/api/samples/create/{id_task}", tags=["Samples"], response_model=SampleResponse
)
async def create_sample(
    id_task: int, file: UploadFile, db: Annotated[Session, Depends(get_db)]
):
    sample_service = SampleService(db)
    file_content = await file.read()
    sample = sample_service.create_sample(file_content, file.content_type, id_task)
    return SampleResponse(id=sample.id, id_task=sample.id_task, id_user=sample.id_user)
