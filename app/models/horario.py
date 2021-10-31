from app import db
from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

class Horario(db.Model):
    __tablename__ = "horario"

    id = Column(Integer, primary_key=True, autoincrement=True)

    am_inicio = Column(Time, nullable=False)
    am_fim = Column(Time)
    pm_inicio = Column(Time)
    pm_fim = Column(Time, nullable=False)
    intervalo = Column(Time, nullable=False)
    almoco = Column(Boolean)
    dia_semana = Column(Integer)

    id_clinica = Column(Integer, ForeignKey('clinica.id'), nullable=False)

    clinica = relationship('Clinica', back_populates='horarios')

    def __init__(self, am_inicio, am_fim, pm_inicio, pm_fim, intervalo, almoco, dia_semana):
        self.am_inicio = am_inicio
        self.am_fim = am_fim
        self.pm_inicio = pm_inicio
        self.pm_fim = pm_fim
        self.intervalo = intervalo
        self.almoco = almoco
        self.dia_semana = dia_semana

    def to_json(self):
        return {"id":self.id, "am_inicio":self.am_inicio, "am_fim":self.am_fim, "pm_inicio":self.pm_incio, "pm_fim":self.pm_fim, "intervalo":self.intervalo, "almoco":self.almoco, "dia_semana":self.dia_semana}

