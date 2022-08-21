from datetime import datetime, timedelta
from dateutil.parser import isoparse

from sqlalchemy import select, Column, ForeignKey, Integer, SmallInteger, String, DateTime, Boolean
from sqlalchemy.orm import relationship, validates

from . import db, session, TimestampMixin
from .horario import Horario
from ..exceptions import APIException


class Consulta(TimestampMixin, db.Model):
    __tablename__ = "consulta"

    descricao = Column(String(255))
    marcada = Column(DateTime, nullable=False)
    duracao = Column(SmallInteger, nullable=False)
    realizada = Column(Boolean, default=False)
    patient_id = Column(Integer, ForeignKey('patients.id'), nullable=False)
    clinic_id = Column(Integer, ForeignKey('clinics.id'), nullable=False)

    patient = relationship("Patient", back_populates="consultas")

    def __init__(self, **kw):
        marcada = kw["marcada"]

        _, horario = self.verifica_marcada(marcada, kw["clinic_id"])
        del kw["marcada"]

        if not kw.get("duracao"):
            kw["duracao"] = horario.intervalo.total_seconds() if horario else 0

        super().__init__(**kw, marcada=marcada)

    def as_json(self):
        obj_json = super().as_json()

        del obj_json["created_at"]
        del obj_json["updated_at"]

        return obj_json

    def verifica_marcada(self, marcada, clinic_id):
        """
        Verifica se a clinic existe e os horários
        """
        if not isinstance(marcada, datetime):
            try:
                marcada = isoparse(marcada)
            except ValueError as error:
                raise APIException(
                    "date and time is not a string in iso format",
                    detail={"marcada": "invalid"}) from error
            except Exception as error:
                raise error

        clinic = session.execute(select(
            clinic.id).filter_by(id=clinic_id)).scalar()

        if clinic is None:
            raise APIException("clinic_id is not a id of a clinic",
                               detail={"clinic_id": "invalid"})

        weekday = marcada.weekday()

        horario = session.execute(
            select(Horario).filter_by(clinic_id=clinic,
                                      dia_semana=weekday)).scalar()
        return marcada, horario

    @validates('marcada')
    def valida_marcada(self, _, marcada):
        """
        Valida se uma consulta marcada é válida
        """
        marcada, horario = self.verifica_marcada(marcada, self.clinic_id)

        if horario is not None:
            hora = marcada.time()

            if hora < horario.am_inicio or (
                    horario.am_fim and hora >= horario.am_fim
                    and hora < horario.pm_inicio) or hora >= horario.pm_fim:
                marcada = None
                print(horario.as_dict())
            else:
                exists = session.execute(
                    select(Consulta.id).filter_by(
                        clinic_id=self.clinic_id).filter(
                            Consulta.id != self.id).filter(
                                Consulta.marcada >= marcada, Consulta.marcada <
                                (marcada +
                                 timedelta(seconds=self.duracao)))).scalar()

        if (not horario or marcada is None or exists is not None):
            raise APIException("This date and time are not valid",
                               detail={"marcada": "invalid"})

        return marcada
