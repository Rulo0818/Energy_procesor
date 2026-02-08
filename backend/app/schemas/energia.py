from datetime import date
from decimal import Decimal
from typing import List

from pydantic import BaseModel, field_validator


class EnergiaExcedenteResponse(BaseModel):
    id: int
    cups_cliente: str
    instalacion_gen: str
    fecha_desde: date
    fecha_hasta: date
    tipo_autoconsumo: int
    energia_neta_gen: List[Decimal]
    energia_autoconsumida: List[Decimal]
    pago_tda: List[Decimal]

    @field_validator("energia_neta_gen", "energia_autoconsumida", "pago_tda")
    @classmethod
    def validar_longitud_arrays(cls, v: List) -> List:
        if len(v) != 6:
            raise ValueError("Cada array debe contener exactamente 6 valores (P1-P6)")
        return v

    model_config = {"from_attributes": True}


class EnergiaListResponse(BaseModel):
    total: int
    registros: List[EnergiaExcedenteResponse]
