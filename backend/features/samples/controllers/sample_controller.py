from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..schemas.sample_schema import SampleListResponse, SampleResponse
from ..services.sample_service import SampleService
from ...authorization.services.token_service import TokenService, UserData


router = APIRouter()


@router.post(
    "/api/samples/upload/{id_package}",
    tags=["Samples"],
    response_model=SampleListResponse,
)
async def create_samples(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    files: list[UploadFile],
    db: Annotated[Session, Depends(get_db)],
):
    sample_service = SampleService(db)
    response = SampleListResponse(samples=[])

    for file in files:
        file_content = await file.read()
        sample = sample_service.create_sample(
            file_content, file.content_type, id_package
        )
        response.samples.append(
            SampleResponse(id=sample.id, id_package=sample.id_package)
        )

    return response
