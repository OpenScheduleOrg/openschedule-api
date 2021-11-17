from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import db, TimestampMixin

class Clinica(TimestampMixin, db.Model):
    __tablename__ = "clinica"

    nome = Column(String(255), nullable=False)
    tipo = Column(String(255))
    telefone = Column(String(11), nullable=False)
    endereco = Column(String(255), nullable=False)
    longitude = Column(String(45))
    latitude = Column(String(45))

    consultas = relationship("Consulta", back_populates="clinica")
    horarios = relationship("Horario", back_populates="clinica")


