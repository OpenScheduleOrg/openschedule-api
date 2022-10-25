from sqlalchemy import Column, ForeignKey, SmallInteger, Integer, Date

from . import db, TimestampMixin
from ..validations import Validator


class Schedule(TimestampMixin, db.Model):
    __tablename__ = "schedules"

    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    start_time = Column(SmallInteger, nullable=False)
    end_time = Column(SmallInteger, nullable=False)
    max_visits = Column(SmallInteger, nullable=False, default=1)
    week_day = Column(SmallInteger)

    acting_id = Column(Integer, ForeignKey('actuations.id'), nullable=False)

    validators = {
        "start_date": Validator("start_date").required().date(),
        "end_date": Validator("end_date").date(),
        "start_time": Validator("start_time").required().number(),
        "end_time": Validator("end_time").required().number(),
        "max_visits": Validator("max_visits").number(),
        "week_day": Validator("week_day").number().range(0, 6),
        "acting_id": Validator("acting_id").required()
    }
