from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.models import db

class Horario(db.Model):
    __tablename__ = "horario"

    am_inicio = Column(Time, nullable=False)
    am_fim = Column(Time)
    pm_inicio = Column(Time)
    pm_fim = Column(Time, nullable=False)
    intervalo = Column(Time, nullable=False)
    almoco = Column(Boolean)
    dia_semana = Column(Integer, nullable=False)

    id_clinica = Column(Integer, ForeignKey('clinica.id'), nullable=False)

    clinica = relationship('Clinica', back_populates='horarios')


