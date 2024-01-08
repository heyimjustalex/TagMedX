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

    def check_if_assigned_to_user(self, id_user: int, package: Package):
        if package.id_user != id_user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="This package is not assigned to this user",
            )

    def assign_to_user(self, package: Package, id_user: int) -> Package:
        package.id_user = id_user
        self.repository.update()
        return package

    def mark_as_ready(self, package: Package) -> Package:
        package.is_ready = True
        self.repository.update()
        return package

    def mark_as_unready(self, package: Package) -> Package:
        package.is_ready = False
        self.repository.update()
        return package

    def delete_package(self, package: Package):
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

    def get_user_packages_in_set(self, id_set: int, id_user: int) -> list[Package]:
        return self.repository.get_packages_by_set_and_user(id_set, id_user)

    def get_user_packages(self, id_user: int) -> list[Package]:
        return self.repository.get_packages_by_user(id_user)

    def get_packages_in_group(self, id_group: int) -> list[Package]:
        return self.repository.get_packages_by_group(id_group)

    def get_user_packages_in_group(self, id_group: int, id_user: int) -> list[Package]:
        return self.repository.get_packages_by_group_and_user(id_group, id_user)

    def get_package_id_with_free_slots_or_create_new_one(self, id_set: int) -> int:
        packages = self.get_packages_in_set(id_set)
        for package in packages:
            if len(package.Sample) < package.Set.package_size:
                return package.id
        return self.create_package(id_set).id

    def all_samples_examinated(self, package: Package) -> bool:
        for sample in package.Sample:
            if not sample.Examination:
                return False
        return True

    def count_packages_in_group(
        self, id_group: int, id_user: int | None = None, is_ready: bool | None = None
    ) -> int:
        if id_user is not None and is_ready is not None:
            return self.repository.count_packages_by_group_user_and_readiness(
                id_group, id_user, is_ready
            )
        elif is_ready is not None:
            return self.repository.count_packages_by_group_and_readiness(
                id_group, is_ready
            )
        elif id_user is not None:
            return self.repository.count_packages_by_group_and_user(id_group, id_user)
        return self.repository.count_packages_by_group(id_group)
