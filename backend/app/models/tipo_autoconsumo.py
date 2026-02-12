from sqlalchemy import Column, Integer, String, Boolean, CheckConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class TipoAutoconsumo(Base):
    __tablename__ = "tipo_autoconsumo"

    codigo = Column(Integer, primary_key=True)
    descripcion = Column(String(255), nullable=False)
    activo = Column(Boolean, default=True)

    registros_energia = relationship("EnergiaExcedentaria", back_populates="tipo")

    __table_args__ = (
        CheckConstraint("codigo IN (12, 41, 42, 43, 51)", name="ck_tipos_validos"),
    )
