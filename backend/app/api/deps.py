from typing import Generator

from sqlalchemy.orm import Session

from app.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """Dependencia FastAPI para obtener sesión de BD."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
