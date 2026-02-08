from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.api.deps import get_db
from app.models import ArchivoProcesado, EnergiaExcedentaria, RegistroErrores

router = APIRouter(prefix="/api/v1/stats", tags=["stats"])


@router.get("")
def get_stats(db: Session = Depends(get_db)):
    """Estadísticas para el dashboard."""
    total_archivos = db.query(func.count(ArchivoProcesado.id)).scalar() or 0
    total_energia = db.query(func.count(EnergiaExcedentaria.id)).scalar() or 0
    total_errores = db.query(func.count(RegistroErrores.id)).scalar() or 0
    return {
        "total_archivos": total_archivos,
        "total_registros_energia": total_energia,
        "total_errores": total_errores,
    }
