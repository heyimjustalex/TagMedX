import os
from uuid import uuid4
from sqlalchemy.orm import Session
from repositories.sample_repository import SampleRepository
from models.models import Sample
from fastapi import HTTPException, status

IMAGE_TYPES = {"image/jpeg": "jpg", "image/png": "png"}


class SampleService:
    def __init__(self, db: Session) -> None:
        self.repository: SampleRepository = SampleRepository(db)

    def create_sample(
        self, file_content: bytes, content_type: str | None, id_package: int
    ) -> Sample:
        if not content_type:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="The file type is not specified.",
            )

        if content_type not in IMAGE_TYPES.keys():
            raise HTTPException(
                status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                detail=f"The {content_type} file type is not supported.",
            )

        path = f"/images/package{id_package}_{uuid4()}.{IMAGE_TYPES.get(content_type)}"
        with open(path, "wb") as image_file:
            image_file.write(file_content)

        sample = Sample()
        sample.id_package = id_package
        sample.path = path
        sample.format = content_type

        self.repository.create_sample(sample)
        return sample

    def delete_sample(self, id_sample: int):
        sample = self.get_sample(id_sample)
        os.remove(sample.path)
        self.repository.delete_sample(sample)

    def get_sample(self, id_sample: int) -> Sample:
        sample = self.repository.get_sample_by_id(id_sample)
        if not sample:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Sample not found"
            )
        return sample

    def get_samples_in_package(self, id_package: int) -> list[Sample]:
        return self.repository.get_samples_by_package(id_package)

    def get_user_samples(self, id_user: int) -> list[Sample]:
        return self.repository.get_samples_by_user(id_user)
