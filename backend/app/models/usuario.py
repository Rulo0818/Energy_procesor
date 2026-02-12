from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class Usuario(Base):
    __tablename__ = "usuario"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True, index=True)
    email = Column(String(255), nullable=False, unique=True, index=True)
    password_hash = Column(String(255), nullable=False)
    nombre_completo = Column(String(255), nullable=False)
    rol = Column(String(20), nullable=False, default="operador")
    activo = Column(Boolean, default=True)
    fecha_registro = Column(DateTime, nullable=False, server_default=func.now())
    ultima_sesion = Column(DateTime, nullable=True)

    archivos = relationship("ArchivoProcesado", back_populates="usuario")
