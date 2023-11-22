from fastapi import APIRouter, Depends, UploadFile
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..schemas.sample_schema import SampleListResponse, SampleResponse
from ..services.sample_service import SampleService
from ...authorization.services.token_service import TokenService, UserData
from ...sets.services.set_service import SetService
from ...groups.services.group_service import GroupService
from ...packages.services.package_service import PackageService


router = APIRouter()


@router.post(
    "/api/samples/upload/{id_set}",
    tags=["Samples"],
    response_model=SampleListResponse,
)
async def create_samples(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_set: int,
    files: list[UploadFile],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set_by_id(id_set)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set.id_group)

    package_service = PackageService(db)
    sample_service = SampleService(db)

    response = SampleListResponse(samples=[])
    for file in files:
        id_package = package_service.get_package_id_with_free_slots_or_create_new_one(
            set.id
        )
        file_content = await file.read()
        sample = sample_service.create_sample(
            file_content, file.content_type, id_package
        )
        response.samples.append(
            SampleResponse(id=sample.id, id_package=sample.id_package)
        )

    return response
