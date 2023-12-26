from sqlalchemy.orm import Session
from models.models import Examination, Sample, Set, Package


class ExaminationRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create_examination(self, examination: Examination):
        self.db.add(examination)
        self.db.commit()

    def update(self):
        self.db.commit()

    def delete_examination(self, examination: Examination):
        self.db.delete(examination)
        self.db.commit()

    def get_examination_by_id(self, id_examination: int) -> Examination | None:
        return (
            self.db.query(Examination).filter(Examination.id == id_examination).first()
        )

    def get_examinations_by_user(self, id_user: int) -> list[Examination]:
        return self.db.query(Examination).filter(Examination.id_user == id_user).all()

    def get_examination_by_sample(self, id_sample: int) -> Examination | None:
        return (
            self.db.query(Examination)
            .filter(Examination.id_sample == id_sample)
            .first()
        )

    def count_examinations_by_package(self, id_package: int) -> int:
        return (
            self.db.query(Examination)
            .filter(Examination.Sample.has(Sample.id_package == id_package))
            .count()
        )

    def count_examinations_by_package_and_tentative(
        self, id_package: int, tentative: bool
    ) -> int:
        return (
            self.db.query(Examination)
            .filter(
                Examination.Sample.has(Sample.id_package == id_package),
                Examination.tentative == tentative,
            )
            .count()
        )

    def count_examinations_by_group(self, id_group: int) -> int:
        return (
            self.db.query(Examination)
            .filter(
                Examination.Sample.has(
                    Sample.Package.has(Package.Set.has(Set.id_group == id_group))
                )
            )
            .count()
        )

    def count_examinations_by_group_and_user(self, id_group: int, id_user: int) -> int:
        return (
            self.db.query(Examination)
            .filter(
                Examination.Sample.has(
                    Sample.Package.has(Package.Set.has(Set.id_group == id_group))
                ),
                Examination.id_user == id_user,
            )
            .count()
        )

    def count_examinations_by_group_and_tentative(
        self, id_group: int, tentative: bool
    ) -> int:
        return (
            self.db.query(Examination)
            .filter(
                Examination.Sample.has(
                    Sample.Package.has(Package.Set.has(Set.id_group == id_group))
                ),
                Examination.tentative == tentative,
            )
            .count()
        )

    def count_examinations_by_group_user_and_tentative(
        self, id_group: int, id_user: int, tentative: bool
    ) -> int:
        return (
            self.db.query(Examination)
            .filter(
                Examination.Sample.has(
                    Sample.Package.has(Package.Set.has(Set.id_group == id_group))
                ),
                Examination.id_user == id_user,
                Examination.tentative == tentative,
            )
            .count()
        )
