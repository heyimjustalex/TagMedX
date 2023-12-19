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

    def delete_examination(self, examination_id: int):
        examination = self.get_examination_by_id(examination_id)
        if examination:
            self.db.delete(examination)
            self.db.commit()

    def get_examination_by_id(self, examination_id: int) -> Examination | None:
        return (
            self.db.query(Examination).filter(Examination.id == examination_id).first()
        )

    def get_examinations_by_user(self, id_user: int) -> Examination | None:
        return self.db.query(Examination).filter(Examination.id_user == id_user).first()

    def get_examination_by_sample(self, sample_id: int) -> Examination | None:
        return (
            self.db.query(Examination)
            .filter(Examination.id_sample == sample_id)
            .first()
        )
