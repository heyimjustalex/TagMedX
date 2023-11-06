from sqlalchemy.orm import Session
from repositories.sample_repository import SampleRepository
from models.models import Sample


class SampleService:
    def __init__(self, db: Session) -> None:
        self.repository: SampleRepository = SampleRepository(db)

    def create_sample(
        self, file_content: bytes, content_type: str | None, id_task: int
    ) -> Sample:
        path = "/images/image.jpg"
        with open(path, "wb") as image_file:
            image_file.write(file_content)

        sample = Sample()
        sample.id_task = id_task
        sample.path = path
        sample.format = content_type

        self.repository.create_sample(sample)
        return sample
