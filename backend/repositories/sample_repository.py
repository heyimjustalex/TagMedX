from sqlalchemy.orm import Session
from models.models import Sample


class SampleRepository:
    def __init__(self, db: Session):
        self.db: Session = db

    def create_sample(self, sample: Sample):
        self.db.add(sample)
        self.db.commit()
