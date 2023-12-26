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
        tentative: bool = False,
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
        tentative: bool | None = None,
    ) -> Examination:
        if tentative:
            examination.tentative = tentative

        if id_user:
            examination.id_user = id_user

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

    def get_sample_examination(self, sample_id: int) -> Examination | None:
        examination = self.repository.get_examination_by_sample(sample_id)
        if not examination:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Examination not found"
            )
        return examination

    def count_examinations_in_package(
        self, id_package: int, tentative: bool | None = None
    ) -> int:
        if tentative is not None:
            return self.repository.count_examinations_by_package_and_tentative(
                id_package, tentative
            )
        return self.repository.count_examinations_by_package(id_package)

    def count_examinations_in_group(
        self, id_group: int, id_user: int | None = None, tentative: bool | None = None
    ) -> int:
        if id_user and tentative is not None:
            return self.repository.count_examinations_by_group_user_and_tentative(
                id_group, id_user, tentative
            )
        elif id_user:
            return self.repository.count_examinations_by_group_and_user(
                id_group, id_user
            )
        elif tentative is not None:
            return self.repository.count_examinations_by_group_and_tentative(
                id_group, tentative
            )
        return self.repository.count_examinations_by_group(id_group)
