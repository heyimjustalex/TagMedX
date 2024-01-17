from sqlalchemy.orm import Session
from models.models import Sample, Package, Set


class SampleRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create_sample(self, sample: Sample):
        self.db.add(sample)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_sample(self, sample: Sample):
        self.db.delete(sample)
        self.db.commit()

    def get_sample_by_id(self, id_sample: int) -> Sample | None:
        return self.db.query(Sample).filter(Sample.id == id_sample).first()

    def get_samples_by_package(self, id_package: int) -> list[Sample]:
        return self.db.query(Sample).filter(Sample.id_package == id_package).all()

    def get_samples_from_set(self, set_id: int) -> list[Sample]:
        return (
            self.db.query(Sample)
            .filter(Sample.Package.has(Package.Set.has(Set.id == set_id)))
            .all()
        )

    def get_samples_by_user(self, id_user: int) -> list[Sample]:
        return (
            self.db.query(Sample)
            .filter(Sample.Package.has(Package.id_user == id_user))
            .all()
        )

    def count_samples_by_group(self, id_group: int) -> int:
        return (
            self.db.query(Sample)
            .filter(Sample.Package.has(Package.Set.has(Set.id_group == id_group)))
            .count()
        )

    def count_samples_by_group_and_user(self, id_group: int, id_user: int) -> int:
        return (
            self.db.query(Sample)
            .filter(
                Sample.Package.has(Package.Set.has(Set.id_group == id_group)),
                Sample.Package.has(Package.id_user == id_user),
            )
            .count()
        )

    def count_samples_with_examination_by_group(self, id_group: int) -> int:
        return (
            self.db.query(Sample)
            .filter(
                Sample.Package.has(Package.Set.has(Set.id_group == id_group)),
                Sample.Examination != None,
            )
            .count()
        )

    def count_samples_with_examination_by_group_and_user(
        self, id_group: int, id_user: int
    ) -> int:
        return (
            self.db.query(Sample)
            .filter(
                Sample.Package.has(Package.Set.has(Set.id_group == id_group)),
                Sample.Package.has(Package.id_user == id_user),
                Sample.Examination != None,
            )
            .count()
        )
