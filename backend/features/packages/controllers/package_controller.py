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
from ...examination.services.examination_service import ExaminationService
from ...groups.services.group_service import GroupService
from ...sets.services.set_service import SetService
from repositories.group_repository import Roles

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

    examination_service = ExaminationService(db)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        all=examination_service.count_examinations_in_package(package.id),
        tentative=examination_service.count_examinations_in_package(
            package.id, tentative=True
        ),
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
    tentative: bool = False,
):
    package_service = PackageService(db)
    package = package_service.get_package(id_package)

    package_service.check_if_assigned_to_user_or_if_user_is_admin(user_data.id, package)

    group_service = GroupService(db)

    examination_service = ExaminationService(db)

    response = ExtendedPackageResponse(
        id=package.id,
        id_set=package.id_set,
        all=examination_service.count_examinations_in_package(package.id),
        tentative=examination_service.count_examinations_in_package(
            package.id, tentative=True
        ),
        id_user=package.id_user,
        is_ready=package.is_ready,
        samples=[],
    )

    for sample in package.Sample:
        sample_response = ExtendedSampleResponse(
            id=sample.id, id_package=sample.id_package
        )

        if tentative == True and (
            not sample.Examination or sample.Examination.tentative != True
        ):
            continue

        if not sample.Examination:
            response.samples.append(sample_response)
            continue

        user = ""

        if sample.Examination.User.title:
            user += f"{sample.Examination.User.title} "

        if sample.Examination.User.name:
            user += f"{sample.Examination.User.name} "

        if sample.Examination.User.surname:
            user += f"{sample.Examination.User.surname}"

        user_role = group_service.get_role_in_group(
            sample.Examination.User.id, package.Set.id_group
        )

        examination_response = ExtendedExaminationResponse(
            id=sample.Examination.id,
            user=user,
            role=user_role,
            id_user=sample.Examination.id_user,
            id_sample=sample.Examination.id_sample,
            tentative=sample.Examination.tentative,
            bboxes=[],
        )

        for bbox in sample.Examination.BBox:
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

        sample_response.examination = examination_response

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
    role = group_service.get_role_in_group(user_data.id, set.id_group)

    package_service = PackageService(db)
    examination_service = ExaminationService(db)

    if role == Roles.ADMIN:
        packages = package_service.get_packages_in_set(set.id)
    else:
        packages = package_service.get_user_packages_in_set(set.id, user_data.id)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                all=examination_service.count_examinations_in_package(package.id),
                tentative=examination_service.count_examinations_in_package(
                    package.id, tentative=True
                ),
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
    package_service = PackageService(db)
    examination_service = ExaminationService(db)

    role = group_service.get_role_in_group(user_data.id, id_group)

    if role == Roles.ADMIN:
        packages = package_service.get_packages_in_group(id_group)
    else:
        packages = package_service.get_user_packages_in_group(id_group, user_data.id)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                all=examination_service.count_examinations_in_package(package.id),
                tentative=examination_service.count_examinations_in_package(
                    package.id, tentative=True
                ),
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
    examination_service = ExaminationService(db)
    package_service = PackageService(db)
    packages = package_service.get_user_packages(user_data.id)

    response: list[PackageResponse] = []
    for package in packages:
        response.append(
            PackageResponse(
                id=package.id,
                id_set=package.id_set,
                all=examination_service.count_examinations_in_package(package.id),
                tentative=examination_service.count_examinations_in_package(
                    package.id, tentative=True
                ),
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

    package = package_service.assign_to_user(package, id_user)

    examination_service = ExaminationService(db)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        all=examination_service.count_examinations_in_package(package.id),
        tentative=examination_service.count_examinations_in_package(
            package.id, tentative=True
        ),
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
    examination_service = ExaminationService(db)
    package_service = PackageService(db)
    package = package_service.get_package(id_package)
    package_service.check_if_assigned_to_user_or_if_user_is_admin(user_data.id, package)
    package = package_service.mark_as_ready(package)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        all=examination_service.count_examinations_in_package(package.id),
        tentative=examination_service.count_examinations_in_package(
            package.id, tentative=True
        ),
        id_user=package.id_user,
        is_ready=package.is_ready,
    )


@router.put(
    "/api/packages/{id_package}/unready",
    tags=["Packages"],
    response_model=PackageResponse,
)
async def mark_as_unready(
    user_data: Annotated[UserData, Depends(TokenService.get_user_data)],
    id_package: int,
    db: Annotated[Session, Depends(get_db)],
):
    examination_service = ExaminationService(db)
    package_service = PackageService(db)
    package = package_service.get_package(id_package)
    package_service.check_if_assigned_to_user_or_if_user_is_admin(user_data.id, package)
    package = package_service.mark_as_unready(package)

    return PackageResponse(
        id=package.id,
        id_set=package.id_set,
        all=examination_service.count_examinations_in_package(package.id),
        tentative=examination_service.count_examinations_in_package(
            package.id, tentative=True
        ),
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

    package_service.delete_package(package)
    return {"message": "Package removed successfully"}
