from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..schemas.sample_schema import SampleResponse
from ..services.sample_service import SampleService
from ...authorization.services.token_service import TokenService, UserData
from ...sets.services.set_service import SetService
from ...groups.services.group_service import GroupService
from ...packages.services.package_service import PackageService


router = APIRouter()


@router.post(
    "/api/samples/upload/{id_set}",
    tags=["Samples"],
    response_model=list[SampleResponse],
)
async def create_samples(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_set: int,
    files: list[UploadFile],
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, set.id_group)

    package_service = PackageService(db)
    sample_service = SampleService(db)

    response: list[SampleResponse] = []
    for file in files:
        id_package = package_service.get_package_id_with_free_slots_or_create_new_one(
            set.id
        )
        file_content = await file.read()
        sample = sample_service.create_sample(
            file_content, file.content_type, id_package
        )
        response.append(SampleResponse(id=sample.id, id_package=sample.id_package))

    return response


@router.get(
    "/api/samples/{id_sample}",
    tags=["Samples"],
    response_class=FileResponse,
)
async def get_sample(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_sample: int,
    db: Annotated[Session, Depends(get_db)],
):
    sample_service = SampleService(db)
    sample = sample_service.get_sample(id_sample)

    group_service = GroupService(db)
    _ = group_service.get_membership(sample.Package.Set.id_group, user_data.id)

    return sample.path


@router.get("/api/samples", tags=["Samples"], response_model=list[SampleResponse])
async def get_user_samples(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    sample_service = SampleService(db)
    samples = sample_service.get_user_samples(user_data.id)

    response: list[SampleResponse] = []
    for sample in samples:
        response.append(SampleResponse(id=sample.id, id_package=sample.id_package))

    return response


@router.get(
    "/api/samples/package/{id_package}",
    tags=["Samples"],
    response_model=list[SampleResponse],
)
async def get_samples_in_package(
    id_package: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    group_service = GroupService(db)
    _ = group_service.get_membership(package.Set.id_group, user_data.id)

    sample_service = SampleService(db)
    samples = sample_service.get_samples_in_package(package.id)

    response: list[SampleResponse] = []
    for sample in samples:
        response.append(SampleResponse(id=sample.id, id_package=sample.id_package))

    return response


@router.delete("/api/samples/{id_sample}", tags=["Samples"])
async def delete_sample(
    id_sample: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    sample_service = SampleService(db)
    sample = sample_service.get_sample(id_sample)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, sample.Package.Set.id_group)

    sample_service.delete_sample(sample.id)
    return {"message": "Sample removed successfully"}
