from sqlalchemy.orm import Session

from app.models import ArchivoProcesado


def obtener_archivo_por_hash(db: Session, hash_archivo: str) -> ArchivoProcesado | None:
    """Comprueba si ya existe un archivo con el mismo hash (duplicado)."""
    return (
        db.query(ArchivoProcesado).filter(ArchivoProcesado.hash_archivo == hash_archivo).first()
    )
