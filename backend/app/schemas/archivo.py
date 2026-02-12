from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ArchivoUploadResponse(BaseModel):
    archivo_id: int
    nombre_archivo: str
    estado: str
    mensaje: str


class ArchivoStatus(BaseModel):
    id: int
    usuario_id: int
    nombre_archivo: str
    fecha_carga: datetime
    estado: str
    total_registros: int
    registros_exitosos: int
    registros_con_error: int

    model_config = {"from_attributes": True}
