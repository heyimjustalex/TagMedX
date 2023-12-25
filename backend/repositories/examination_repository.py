from sqlalchemy.orm import Session
from models.models import Examination


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
