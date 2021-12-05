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
            if isinstance(value, (date, time,)):
                obj_dict[key] = value.isoformat()
            elif isinstance(value, timedelta):
                obj_dict[key] = str(value)
            elif isinstance(value, tuple):
                obj_dict[key] = list(value)

        return obj_dict

class TimestampMixin(object):
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)

def result_to_json(result, first=False, **serialize):
    """
    :result Result
    """
    if first:
        row = result.first()
        if(row):
            row_asdict = row._asdict()
            for key, method in serialize.items():
                row_asdict[key] = getattr(row_asdict[key], method)()
            return row_asdict

        return row

    rows = list()

    for row in result:
        row_asdict = row._asdict()

        for key, method in serialize.items():
            row_asdict[key] = getattr(row_asdict[key], method)()

        rows.append(row_asdict)
    return rows


db = SQLAlchemy(model_class=DefaultModel)
session = db.session
select = db.select
delete = db.delete
insert = db.insert
update = db.update

from app.models.cliente import Cliente
from app.models.clinica import Clinica
from app.models.horario import Horario
from app.models.consulta import Consulta
