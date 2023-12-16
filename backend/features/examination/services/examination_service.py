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
        to_further_verification: bool | None = None,
        bad_quality: bool | None = None,
    ) -> Examination:
        examination = Examination()

        examination.id_user == id_user
        examination.id_sample == id_sample
        examination.to_further_verification == to_further_verification
        examination.bad_quality == bad_quality

        self.repository.create_examination(examination)
        return examination

    def update_examination(
        self,
        examination: Examination,
        to_further_verification: bool | None = None,
        bad_quality: bool | None = None,
    ) -> Examination:
        if to_further_verification:
            examination.to_further_verification = to_further_verification

        if bad_quality:
            examination.bad_quality = bad_quality

        self.repository.update()
        return examination

    def delete_examination(self, examination: Examination):
        self.repository.delete_examination(examination)

    def get_examination(self, id_examination: int) -> Examination:
        examination = self.repository.get_examination_by_id(id_examination)
        if not examination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Examination not found"
            )
        return examination

    def get_user_examinations(self, id_user: int) -> list[Examination]:
        return self.repository.get_examinations_by_user(id_user)

    def get_sample_examinations(self, id_sample: int) -> list[Examination]:
        return self.repository.get_examinations_by_sample(id_sample)
