from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models import ArchivoProcesado, RegistroErrores
from app.schemas.error import ErrorResponse

router = APIRouter(tags=["errores"])


@router.get("", response_model=list[ErrorResponse])
def get_todos_errores(db: Session = Depends(get_db)):
    """Obtiene todos los errores registrados."""
    errores = (
        db.query(RegistroErrores)
        .order_by(RegistroErrores.archivo_id, RegistroErrores.linea_archivo)
        .all()
    )
    return [ErrorResponse.model_validate(e) for e in errores]


@router.get("/{archivo_id}", response_model=list[ErrorResponse])
def get_errores_archivo(archivo_id: int, db: Session = Depends(get_db)):
    """Obtiene los errores registrados para un archivo procesado."""
    archivo = db.query(ArchivoProcesado).filter(ArchivoProcesado.id == archivo_id).first()
    if not archivo:
        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    errores = (
        db.query(RegistroErrores)
        .filter(RegistroErrores.archivo_id == archivo_id)
        .order_by(RegistroErrores.linea_archivo)
        .all()
    )
    return [ErrorResponse.model_validate(e) for e in errores]
