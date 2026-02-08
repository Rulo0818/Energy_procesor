"""Tareas Celery para procesamiento asíncrono."""

from app.celery_app import celery_app
from app.database import SessionLocal
from app.services.procesador_service import procesar_archivo


@celery_app.task(bind=True, name="procesar_archivo")
def procesar_archivo_task(self, archivo_id: int, ruta_archivo: str) -> dict:
    """
    Tarea asíncrona: procesa un archivo de peajes.
    El worker ejecuta esta tarea cuando la API encola un archivo.
    """
    db = SessionLocal()
    try:
        procesar_archivo(db, archivo_id, ruta_archivo)
        return {"archivo_id": archivo_id, "estado": "completado"}
    finally:
        db.close()
