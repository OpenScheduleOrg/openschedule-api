from datetime import date

from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from . import db, TimestampMixin

class Cliente(TimestampMixin, db.Model):
    __tablename__ = "cliente"

    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False)
    cpf = Column(String(11), nullable=False)
    telefone = Column(String(10), nullable=False)
    endereco = Column(String(255), default=None)
    nascimento = Column(Date, default=None)

    consultas = relationship("Consulta", back_populates="cliente")

    def _asjson(self, complete=False, consultas=False):
        obj_json = super()._asjson()

        del obj_json["created_at"]
        del obj_json["updated_at"]

        return obj_json


