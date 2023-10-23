from sqlalchemy.orm import Session
from collections.abc import Generator
from .database import create_database_connection


def get_db() -> Generator[Session, None, None]:
    db = create_database_connection()
    try:
        yield db
    finally:
        db.close()
