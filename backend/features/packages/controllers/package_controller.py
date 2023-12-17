from fastapi import APIRouter, Depends
from ..schemas.package_schema import PackageResponse, ExtendedPackageResponse
from ...samples.schemas.sample_schema import ExtendedSampleResponse
from ...examination.schemas.examination_schema import ExtendedExaminationResponse
from ...bbox.schemas.bbox_schema import ExtendedBBoxResponse
from ...label.schemas.label_schema import LabelResponse
from ...authorization.services.token_service import UserData, TokenService
from typing import Annotated
from connectionDB.session import get_db
from sqlalchemy.orm import Session
from ..services.package_service import PackageService
from ...groups.services.group_service import GroupService
from ...sets.services.set_service import SetService

router = APIRouter()


@router.get(
    "/api/packages/{id_package}", tags=["Packages"], response_model=PackageResponse
)
async def get_package(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    group_service = GroupService(db)
    _ = group_service.get_membership(package.Set.id_group, user_data.id)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        id_user=package.id_user,
        is_ready=package.is_ready,
    )


@router.get(
    "/api/packages/{id_package}/extend",
    tags=["Packages"],
    response_model=ExtendedPackageResponse,
)
async def get_extended_package(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    group_service = GroupService(db)
    _ = group_service.get_membership(package.Set.id_group, user_data.id)

    response = ExtendedPackageResponse(
        id=package.id,
        id_set=package.id_set,
        id_user=package.id_user,
        is_ready=package.is_ready,
        samples=[],
    )

    for sample in package.Sample:
        sample_response = ExtendedSampleResponse(
            id=sample.id, id_package=sample.id_package, examinations=[]
        )

        for examination in sample.Examination:
            examination_response = ExtendedExaminationResponse(
                id=examination.id,
                id_user=examination.id_user,
                id_sample=examination.id_sample,
                tentative=examination.tentative,
                bad_quality=examination.bad_quality,
                bboxes=[],
            )

            for bbox in examination.BBox:
                bbox_response = ExtendedBBoxResponse(
                    id=bbox.id,
                    id_examination=bbox.id_examination,
                    id_label=bbox.id_label,
                    comment=bbox.comment,
                    x=bbox.x,
                    y=bbox.y,
                    width=bbox.width,
                    height=bbox.height,
                    label=LabelResponse(
                        id=bbox.Label.id,
                        id_set=bbox.Label.id_set,
                        name=bbox.Label.name,
                        description=bbox.Label.description,
                        color=bbox.Label.color,
                    ),
                )
                examination_response.bboxes.append(bbox_response)

            sample_response.examinations.append(examination_response)

        response.samples.append(sample_response)

    return response


@router.get(
    "/api/packages/set/{id_set}",
    tags=["Packages"],
    response_model=list[PackageResponse],
)
async def get_packages_in_set(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_set: int,
    db: Annotated[Session, Depends(get_db)],
):
    set_service = SetService(db)
    set = set_service.get_set(id_set)

    group_service = GroupService(db)
    _ = group_service.get_membership(set.id_group, user_data.id)

    package_service = PackageService(db)
    packages = package_service.get_packages_in_set(set.id)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                id_user=package.id_user,
                is_ready=package.is_ready,
            )
        )

    return response


@router.get(
    "/api/packages/group/{id_group}",
    tags=["Packages"],
    response_model=list[PackageResponse],
)
async def get_packages_in_group(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_group: int,
    db: Annotated[Session, Depends(get_db)],
):
    group_service = GroupService(db)
    _ = group_service.get_membership(id_group, user_data.id)

    package_service = PackageService(db)
    packages = package_service.get_packages_in_group(id_group)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                id_user=package.id_user,
                is_ready=package.is_ready,
            )
        )

    return response


@router.get("/api/packages", tags=["Packages"], response_model=list[PackageResponse])
async def get_user_packages(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    packages = package_service.get_user_packages(user_data.id)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                id_user=package.id_user,
                is_ready=package.is_ready,
            )
        )

    return response


@router.put(
    "/api/packages/{id_package}/user/{id_user}",
    tags=["Packages"],
    response_model=PackageResponse,
)
async def assign_to_user(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    id_user: int,
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, package.Set.id_group)
    _ = group_service.get_membership(package.Set.id_group, id_user)

    package = package_service.assign_to_user(id_package, id_user)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        id_user=package.id_user,
        is_ready=package.is_ready,
    )


@router.put(
    "/api/packages/{id_package}/ready",
    tags=["Packages"],
    response_model=PackageResponse,
)
async def mark_as_ready(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.mark_as_ready(user_data.id, id_package)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        id_user=package.id_user,
        is_ready=package.is_ready,
    )


@router.delete("/api/packages/{id_package}", tags=["Packages"])
async def delete_package(
    id_package: int,
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    db: Annotated[Session, Depends(get_db)],
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    group_service = GroupService(db)
    _ = group_service.check_if_admin(user_data.id, package.Set.id_group)

    package_service.delete_package(package.id)
    return {"message": "Package removed successfully"}
