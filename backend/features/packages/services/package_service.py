import os
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from repositories.package_repository import PackageRepository
from models.models import Package


class PackageService:
    def __init__(self, db: Session):
        self.repository = PackageRepository(db)

    def create_package(self, id_set: int) -> Package:
        package = Package()
        package.id_set = id_set
        self.repository.create_package(package)
        return package

    def check_if_assigned_to_user(self, id_user: int, id_package: int):
        package = self.get_package(id_package)
        if package.id_user != id_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This package is not assigned to this user",
            )

    def assign_to_user(self, id_package: int, id_user: int) -> Package:
        package = self.get_package(id_package)
        package.id_user = id_user
        self.repository.update()
        return package

    def mark_as_ready(self, id_user: int, id_package: int) -> Package:
        package = self.get_package(id_package)
        if id_user != package.id_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="It is not possible to mark another user's package as ready",
            )
        package.is_ready = True
        self.repository.update()
        return package

    def delete_package(self, id_package: int):
        package = self.get_package(id_package)
        for sample in package.Sample:
            os.remove(sample.path)
        self.repository.delete_package(package)

    def get_package(self, id_package: int) -> Package:
        package = self.repository.get_package_by_id(id_package)
        if not package:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Package not found"
            )
        return package

    def get_packages_in_set(self, id_set: int) -> list[Package]:
        return self.repository.get_packages_by_set(id_set)

    def get_user_packages(self, id_user: int) -> list[Package]:
        return self.repository.get_packages_by_user(id_user)

    def get_packages_in_group(self, id_group: int) -> list[Package]:
        return self.repository.get_packages_by_group(id_group)

    def get_package_id_with_free_slots_or_create_new_one(self, id_set: int) -> int:
        # package = self.repository.get_package_with_free_slots_by_set(id_set)
        # if not package:
        #     return self.create_package(id_set).id
        # return package.id
        packages = self.get_packages_in_set(id_set)
        for package in packages:
            if len(package.Sample) < package.Set.package_size:
                return package.id
        return self.create_package(id_set).id
