from datetime import datetime, date, time, timedelta

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.orm import DeclarativeBase
from .enums import ClinicType


class DefaultModel(DeclarativeBase):

    id = Column(Integer, primary_key=True)

    def as_dict(self):
        """
            Model to json
        """
        obj_dict = dict(**self.__dict__)

        del obj_dict["_sa_instance_state"]

        return obj_dict

    def as_json(self):
        """
            Model to json
        """
        obj_dict = self.as_dict()

        for key, value in obj_dict.items():
            if isinstance(value, (
                    date,
                    time,
            )):
                obj_dict[key] = value.isoformat()
            elif isinstance(value, timedelta):
                obj_dict[key] = str(value)
            elif isinstance(value, tuple):
                obj_dict[key] = list(value)

        return obj_dict


class TimestampMixin():
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, onupdate=datetime.utcnow)


def result_to_json(result, first=False, **serialize):
    """
    :result Result
    """
    if first:
        row = result.first()
        if row:
            row_asdict = row._asdict()
            for key, method in serialize.items():
                row_asdict[key] = method(row_asdict[key])
            return row_asdict

        return row

    rows = []

    for row in result:
        row_asdict = row._asdict()

        for key, method in serialize.items():
            row_asdict[key] = method(row_asdict[key])

        rows.append(row_asdict)
    return rows


db = SQLAlchemy(model_class=DefaultModel)

session = db.session
select = db.select
delete = db.delete
insert = db.insert
update = db.update

from .clinic import Clinic
from .user import User
from .professional import Professional
from .specialty import Specialty
from .acting import Acting
from .schedule import Schedule
from .patient import Patient
from .appointment import Appointment

from .init_data import set_up_data
