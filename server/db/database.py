from datetime import date
from pathlib import Path
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from server.config import DATABASE_URL

if DATABASE_URL.startswith("sqlite:///"):
    db_file_path = DATABASE_URL.replace("sqlite:///", "")
    # Ensure parent directory exists for SQLite file
    Path(db_file_path).parent.mkdir(parents=True, exist_ok=True)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {},
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def create_tables() -> None:
    from server.db import models  # noqa: F401

    Base.metadata.create_all(bind=engine)

    # Automatically seed farm_001 if not present (ensures instant demo readiness on fresh environments)
    db = SessionLocal()
    try:
        existing_farm = db.query(models.Farm).filter_by(farm_id="farm_001").first()
        if not existing_farm:
            demo_farm = models.Farm(
                farm_id="farm_001",
                crop="wheat",
                planting_date=date(2026, 1, 15),
                language="hi-IN",
                state="Punjab",
                district="Ludhiana",
                commodity="Wheat",
                lat=30.9,
                lon=75.8,
            )
            db.add(demo_farm)
            db.commit()
    finally:
        db.close()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
