from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship, validates

from . import db, TimestampMixin
from .clinica  import Clinica
from .horario import Horario
from ..common.exc import APIExceptionHandler


class Consulta(TimestampMixin, db.Model):
    __tablename__ = "consulta"

    marcada = Column(DateTime, nullable=False)
    descricao = Column(String(255))
    realizada = Column(Boolean, default=False)
    id_cliente = Column(Integer, ForeignKey(
        'cliente.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey(
        'clinica.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="consultas")
    clinica = relationship("Clinica", back_populates="consultas")

    def __init__(self, **kw):
        marcada = kw["marcada"]
        del kw["marcada"]

        super().__init__(**kw, marcada=marcada)

    @validates('marcada')
    def validate_marcada(self, key, marcada):

        if not isinstance(marcada, datetime):
            try:
                marcada = datetime.fromisoformat(marcada)
            except ValueError:
                raise APIExceptionHandler("date and time is not a string in iso format", detail={"marcada": "invalid"})
            except Exception as e:
                raise e

        clinica = Clinica.query.get(self.id_clinica)

        if clinica is None:
            raise APIExceptionHandler("id_clinica is not a id of a cliente", detail={"id_clinica": "invalid"})

        weekday = marcada.weekday()

        horario = Horario.query.filter_by(id_clinica=clinica.id, dia_semana=weekday).first()

        if horario is not None:
            hora = marcada.time()

            if hora < horario.am_inicio or ( horario.almoco and (hora >= horario.am_fim and hora < horario.pm_inicio)) or hora >= horario.pm_fim:
                marcada = None
            else:
                exists = Consulta.query.filter_by(marcada=marcada, id_clinica=self.id_clinica).first()

        if(not horario or marcada is None or exists is not None):
            raise APIExceptionHandler("This date and time are not valid", detail={"marcada":"invalid"})

        return marcada



