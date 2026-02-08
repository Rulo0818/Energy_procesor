from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship

from app.database import Base


class TipoAutoconsumo(Base):
    __tablename__ = "tipo_autoconsumo"

    codigo = Column(Integer, primary_key=True)
    descripcion = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)

    registros_energia = relationship("EnergiaExcedentaria", back_populates="tipo")
