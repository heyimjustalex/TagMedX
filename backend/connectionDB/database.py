import os
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_USER = os.getenv("DB_USER")

if not DB_USER:
    raise ValueError("No database user specified (DB_USER environment variable)")

DB_PASSWORD = os.getenv("DB_PASSWORD")

if not DB_PASSWORD:
    raise ValueError(
        "No database password specified (DB_PASSWORD environment variable)"
    )

DB_HOST = os.getenv("DB_HOST")

if not DB_HOST:
    raise ValueError("No database host specified (DB_HOST environment variable)")

DB_PORT = os.getenv("DB_PORT")

if not DB_PORT:
    raise ValueError("No database port specified (DB_PORT environment variable)")

DB_NAME = os.getenv("DB_NAME")

if not DB_NAME:
    raise ValueError("No database name specified (DB_NAME environment variable)")

DATABASE_URL = f"mysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_database_connection() -> Session:
    db = SessionLocal()
    return db
