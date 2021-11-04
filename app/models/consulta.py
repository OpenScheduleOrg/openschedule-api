from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from app.models import db, TimestampMixin

class Consulta(TimestampMixin, db.Model):
    __tablename__ = "consulta"

    marcada = (DateTime)
    descricao = Column(String(255))
    realizada = Column(Boolean)
    id_cliente = Column(Integer, ForeignKey(
        'cliente.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey(
        'clinica.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="consultas")
    clinica = relationship("Clinica", back_populates="consultas")


