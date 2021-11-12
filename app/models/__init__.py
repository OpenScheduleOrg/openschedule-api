from datetime import datetime, date, time, timedelta

from flask_sqlalchemy import Model, SQLAlchemy
from sqlalchemy import Column, Integer, DateTime

class DefaultModel(Model):

    id = Column(Integer, primary_key=True)

    def _asdict(self):
        obj_dict = dict(**self.__dict__)

        del obj_dict["_sa_instance_state"]

        return obj_dict

    def _asjson(self):
        obj_dict = self._asdict()

        for key, value in obj_dict.items():

            if not isinstance(value, (str, int, float, list, tuple, dict, bool)) and value != None:
                obj_dict[key] = str(value)
            elif isinstance(value, tuple):
                obj_dict[key] = list(value)

        return obj_dict

class TimestampMixin(object):
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

db = SQLAlchemy(model_class=DefaultModel)

from app.models.cliente import Cliente
from app.models.clinica import Clinica
from app.models.horario import Horario
from app.models.consulta import Consulta
