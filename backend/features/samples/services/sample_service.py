import os
import numpy as np
from io import BytesIO
from pydicom import dcmread
from PIL import Image
from uuid import uuid4
from sqlalchemy.orm import Session
from repositories.sample_repository import SampleRepository
from models.models import Sample
from fastapi import HTTPException, status
from typing import Literal

IMAGE_TYPES = {
    "image/jpeg": "jpg",
    "image/png": "png",
    "application/octet-stream": "jpg",
}


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

        if content_type == "application/octet-stream":
            try:
                ds = dcmread(BytesIO(file_content), force=True)
                image_array = ds.pixel_array.astype(float)
                scaled_image_array = (
                    np.maximum(image_array, 0) / image_array.max()
                ) * 255.0
                scaled_image_array = np.uint8(scaled_image_array)
                image = Image.fromarray(scaled_image_array)
                image.save(path)
            except Exception as e:
                print(e)
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=f"Error during converting {content_type} type file to jpeg",
                )
        else:
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

    def count_samples_in_group(
        self,
        id_group: int,
        id_user: int | None = None,
        examinated: Literal[True] | None = None,
    ) -> int:
        if id_user and examinated:
            return self.repository.count_samples_with_examination_by_group_and_user(
                id_group, id_user
            )
        elif id_user:
            return self.repository.count_samples_by_group_and_user(id_group, id_user)
        elif examinated:
            return self.repository.count_samples_with_examination_by_group(id_group)
        return self.repository.count_samples_by_group(id_group)
