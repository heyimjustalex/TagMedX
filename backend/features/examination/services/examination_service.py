from sqlalchemy.orm import Session
from repositories.examination_repository import ExaminationRepository
from models.models import Examination
from fastapi import HTTPException, status


class ExaminationService:
    def __init__(self, db: Session):
        self.repository = ExaminationRepository(db)

    def create_examination(
        self,
        id_user: int,
        id_sample: int,
        tentative: bool | None = None,
    ) -> Examination:
        examination = Examination()

        examination.id_user = id_user
        examination.id_sample = id_sample
        examination.tentative = tentative

        self.repository.create_examination(examination)
        return examination

    def update_examination(
        self,
        examination: Examination,
        id_user: int,
        id_sample: int,
        tentative: bool | None = None,
    ) -> Examination:
        if id_sample:
            examination.id_sample = id_sample

        if tentative:
            examination.tentative = tentative

        if id_user:
            examination.id_user = id_user

        self.repository.update()
        return examination

    def delete_examination(self, examination_id: int):
        self.repository.delete_examination(examination_id)

    def get_examination_by_id(self, id_examination: int) -> Examination:
        examination = self.repository.get_examination_by_id(id_examination)
        if not examination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Examination not found"
            )
        return examination

    def get_user_examinations(self, id_user: int) -> Examination | None:
        return self.repository.get_examinations_by_user(id_user)

    def get_examination_by_sample(self, sample_id: int) -> Examination | None:
        return self.repository.get_examination_by_sample(sample_id)
