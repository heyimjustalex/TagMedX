from fastapi import APIRouter, Depends
from ..schemas.package_schema import PackageResponse
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
