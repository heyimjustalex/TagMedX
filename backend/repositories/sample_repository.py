from sqlalchemy.orm import Session
from models.models import Sample, Package


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

    def get_samples_by_user(self, id_user: int) -> list[Sample]:
        return (
            self.db.query(Sample)
            .filter(Sample.Package.has(Package.id_user == id_user))
            .all()
        )
