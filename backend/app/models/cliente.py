from sqlalchemy import Column, Integer, String, Boolean, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import TIMESTAMP

from app.database import Base


class Cliente(Base):
    __tablename__ = "cliente"

    id = Column(Integer, primary_key=True, index=True)
    cups = Column(String(255), nullable=False)
    nombre_cliente = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True)
    telefono = Column(String(255), nullable=True)
    direccion = Column(Text, nullable=True)
    municipio = Column(String(100), nullable=True)
    provincia = Column(String(100), nullable=True)
    codigo_postal = Column(String(100), nullable=True)
    activo = Column(Boolean, default=True)
    fecha_registro = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    fecha_actualizacion = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    registros_energia = relationship("EnergiaExcedentaria", back_populates="cliente")