from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class ClienteBase(BaseModel):
    cups: str = Field(..., min_length=18, max_length=20)
    nombre_cliente: str = Field(..., min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    municipio: Optional[str] = Field(None, max_length=100)
    provincia: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=5)
    activo: bool = True


class ClienteCreate(ClienteBase):
    pass


class ClienteUpdate(BaseModel):
    cups: Optional[str] = Field(None, min_length=18, max_length=20)
    nombre_cliente: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None
    telefono: Optional[str] = Field(None, max_length=20)
    direccion: Optional[str] = None
    municipio: Optional[str] = Field(None, max_length=100)
    provincia: Optional[str] = Field(None, max_length=100)
    codigo_postal: Optional[str] = Field(None, max_length=5)
    activo: Optional[bool] = None


class ClienteResponse(ClienteBase):
    id: int
    fecha_registro: datetime
    fecha_actualizacion: datetime

    class Config:
        from_attributes = True


class ClienteWithStats(ClienteResponse):
    total_registros: int
    total_energia_generada: float
    total_energia_autoconsumida: float
    total_pago_tda: float
