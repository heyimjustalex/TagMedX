from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from models.models import Package, Set, Sample, Package, Examination


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

    def get_package_by_id(self, id_package: int) -> Package | None:
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

    def get_packages_by_group(self, id_group: int) -> list[Package]:
        return (
            self.db.query(Package)
            .filter(Package.Set.has(Set.id_group == id_group))
            .all()
        )

    def update_package_is_ready(self, sample: Sample, package: Package, set_info: Set):
        all_samples_have_examination = (
            self.db.query(Sample)
            .join(Examination, Sample.id == Examination.id_sample)
            .filter(Sample.id_package == sample.id_package)
            .count()
            == set_info.package_size
        )
        if all_samples_have_examination:
            package.is_ready = True
            self.db.commit()
            return True
        else:
            return False

    def update_package_is_ready_false(self, sample_id: int):
        sample = self.db.query(Sample).filter(Sample.id == sample_id).first()
        if sample:
            package = (
                self.db.query(Package).filter(Package.id == sample.id_package).first()
            )

            if package:
                package.is_ready = False
                self.db.commit()
                return True
        return False
