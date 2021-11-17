from datetime import datetime, timedelta

from sqlalchemy import select, Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship, validates
from sqlalchemy.ext.hybrid import hybrid_property

from . import db, session, TimestampMixin
from .clinica  import Clinica
from .horario import Horario
from ..common.exc import APIExceptionHandler


class Consulta(TimestampMixin, db.Model):
    __tablename__ = "consulta"

    marcada = Column(DateTime, nullable=False)
    descricao = Column(String(255))
    realizada = Column(Boolean, default=False)
    cliente_id = Column(Integer, ForeignKey(
        'cliente.id'), nullable=False)
    clinica_id = Column(Integer, ForeignKey(
        'clinica.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="consultas")
    clinica = relationship("Clinica", back_populates="consultas")

    def __init__(self, **kw):
        marcada = kw["marcada"]
        del kw["marcada"]

        super().__init__(**kw, marcada=marcada)

    def _asjson(self, cliente=False):
        obj_json = super()._asjson()

        del obj_json["created_at"]
        del obj_json["updated_at"]

        return obj_json

    @validates('marcada')
    def validate_marcada(self, key, marcada):

        if not isinstance(marcada, datetime):
            try:
                marcada = datetime.fromisoformat(marcada)
            except ValueError:
                raise APIExceptionHandler("date and time is not a string in iso format", detail={"marcada": "invalid"})
            except Exception as e:
                raise e

        clinica = session.execute(select(Clinica.id).filter_by(id=self.clinica_id)).scalar()

        if clinica is None:
            raise APIExceptionHandler("clinica_id is not a id of a clinica", detail={"clinica_id": "invalid"})

        weekday = marcada.weekday()

        horario = session.execute(select(Horario).filter_by(clinica_id=clinica, dia_semana=weekday)).scalar()
        now = datetime.now()

        if horario is not None:
            hora = marcada.time()

            if hora < horario.am_inicio or (horario.almoco and (hora >= horario.am_fim and hora < horario.pm_inicio)) or hora >= horario.pm_fim:
                marcada = None
            else:
                exists = session.execute(select(Consulta.id).filter_by(marcada=marcada, clinica_id=self.clinica_id)).scalar()

        if(not horario or marcada is None or exists is not None):
            raise APIExceptionHandler("This date and time are not valid", detail={"marcada":"invalid"})

        return marcada

