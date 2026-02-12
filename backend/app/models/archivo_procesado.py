from sqlalchemy import Column, Integer, String, DateTime, Text, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database import Base


class ArchivoProcesado(Base):
    __tablename__ = "archivo_procesado"

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuario.id", ondelete="RESTRICT"), nullable=False)
    nombre_archivo = Column(String(255), nullable=False)
    hash_archivo = Column(String(64), nullable=False, unique=True)
    fecha_carga = Column(DateTime, nullable=False, server_default=func.now())
    fecha_procesamiento = Column(DateTime, nullable=True)
    estado = Column(String(20), nullable=False, default="pendiente")
    total_registros = Column(Integer, default=0)
    registros_exitosos = Column(Integer, default=0)
    registros_con_error = Column(Integer, default=0)
    ruta_archivo = Column(Text, nullable=True)

    usuario = relationship("Usuario", back_populates="archivos")
    registros_energia = relationship(
        "EnergiaExcedentaria", back_populates="archivo", cascade="all, delete-orphan"
    )
    errores = relationship(
        "RegistroErrores", back_populates="archivo", cascade="all, delete-orphan"
    )

    __table_args__ = (
        CheckConstraint(
            "estado IN ('pendiente', 'procesando', 'completado', 'error')",
            name="ck_estado",
        ),
    )
