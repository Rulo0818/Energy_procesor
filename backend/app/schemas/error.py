from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    id: int
    archivo_id: int
    linea_archivo: int
    tipo_error: str
    descripcion: str
    datos_linea: Optional[str] = None
    fecha_registro: datetime

    model_config = {"from_attributes": True}
