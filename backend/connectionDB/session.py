from sqlalchemy.orm import Session
from .database import create_database_connection


def get_db() -> Session:
    db = create_database_connection()
    try:
        yield db
    finally:
        db.close()
