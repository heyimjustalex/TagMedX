from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.models import Package, Set, Sample


class PackageRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create_package(self, package: Package):
        self.db.add(package)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_package(self, package: Package):
        self.db.delete(package)
        self.db.commit()

    def get_package_by_id(self, id_package) -> Package | None:
        return self.db.query(Package).filter(Package.id == id_package).first()

    def get_packages_by_set(self, id_set: int) -> list[Package]:
        return self.db.query(Package).filter(Package.id_set == id_set).all()

    def get_package_with_free_slots_by_set(self, id_set: int) -> Package | None:
        return (
            self.db.query(Package)
            .join(Package.Set)
            .join(Package.Sample)
            .filter(Set.id == id_set)
            .group_by(Package.id)
            .having(func.count(Sample.id) < Set.package_size)
            .first()
        )

    def get_packages_by_user(self, id_user: int) -> list[Package]:
        return self.db.query(Package).filter(Package.id_user == id_user).all()
