from datetime import datetime, timedelta
from dateutil.parser import isoparse

from sqlalchemy import select, Column, ForeignKey, Integer, SmallInteger, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship, validates

from . import db, session, TimestampMixin
from .clinica  import Clinica
from .horario import Horario
from ..exceptions import APIExceptionHandler


class Consulta(TimestampMixin, db.Model):
    __tablename__ = "consulta"

    descricao = Column(String(255))
    marcada = Column(DateTime, nullable=False)
    duracao = Column(SmallInteger, nullable=False)
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

        self.getClinicaHorario(marcada,kw["clinica_id"])

        if(not kw.get("duracao")):
            kw["duracao"] = self.horario.intervalo.total_seconds() if self.horario else 0


        super().__init__(**kw, marcada=marcada)

    def _asjson(self, cliente=False):
        obj_json = super()._asjson()

        del obj_json["created_at"]
        del obj_json["updated_at"]

        return obj_json

    def getClinicaHorario(self, marcada, clinica_id):
        if not isinstance(marcada, datetime):
            try:
                marcada = self._marcada = isoparse(marcada)
            except ValueError:
                raise APIExceptionHandler("date and time is not a string in iso format", detail={"marcada": "invalid"})
            except Exception as e:
                raise e
        else:
            self._marcada = marcada


        clinica = session.execute(select(Clinica.id).filter_by(id=clinica_id)).scalar()

        if clinica is None:
            raise APIExceptionHandler("clinica_id is not a id of a clinica", detail={"clinica_id": "invalid"})

        weekday = marcada.weekday()

        self.horario = session.execute(select(Horario).filter_by(clinica_id=clinica, dia_semana=weekday)).scalar()

    @validates('marcada')
    def validate_marcada(self, key, marcada):
        if not hasattr(self, "horario"):
            self.getClinicaHorario(marcada, self.clinica_id)
        horario = self.horario
        marcada = self._marcada

        now = datetime.now()

        if horario is not None:
            hora = marcada.time()

            if hora < horario.am_inicio or (horario.almoco and (hora >= horario.am_fim and hora < horario.pm_inicio)) or hora >= horario.pm_fim:
                marcada = None
            else:
                exists = session.execute(select(Consulta.id).filter_by(marcada=marcada, clinica_id=self.clinica_id)).scalar()

        if(not horario or marcada is None or exists is not None):
            raise APIExceptionHandler("This date and time are not valid", detail={"marcada":"invalid"})

        del self.horario
        del self._marcada

        return marcada

