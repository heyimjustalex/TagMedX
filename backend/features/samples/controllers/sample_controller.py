from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..schemas.sample_schema import SampleResponse
from ..services.sample_service import SampleService


router = APIRouter()


@router.post(
    "/api/samples/create/{id_package}", tags=["Samples"], response_model=SampleResponse
)
async def create_sample(
    id_package: int, file: UploadFile, db: Annotated[Session, Depends(get_db)]
):
    sample_service = SampleService(db)
    file_content = await file.read()
    sample = sample_service.create_sample(file_content, file.content_type, id_package)
    return SampleResponse(id=sample.id, id_package=id_package, id_user=sample.id_user)
