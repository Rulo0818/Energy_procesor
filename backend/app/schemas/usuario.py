from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UsuarioBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    nombre_completo: str = Field(..., min_length=1, max_length=255)
    rol: str = Field(default="operador", pattern="^(admin|operador|consultor)$")
    activo: bool = True


class UsuarioCreate(UsuarioBase):
    password_hash: str = Field(..., min_length=6)


class UsuarioUpdate(BaseModel):
    username: Optional[str] = Field(None, min_length=3, max_length=100)
    email: Optional[EmailStr] = None
    nombre_completo: Optional[str] = Field(None, min_length=1, max_length=255)
    rol: Optional[str] = Field(None, pattern="^(admin|operador|consultor)$")
    activo: Optional[bool] = None
    password_hash: Optional[str] = Field(None, min_length=6)
    ultima_sesion: Optional[datetime] = None


class UsuarioResponse(UsuarioBase):
    id: int
    fecha_registro: datetime
    ultima_sesion: Optional[datetime] = None

    class Config:
        from_attributes = True
