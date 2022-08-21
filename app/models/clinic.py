from sqlalchemy import Column, String, CHAR, Enum, Float

from . import db, TimestampMixin, ClinicType
from ..validations import Validator


class Clinic(TimestampMixin, db.Model):
    __tablename__ = "clinics"

    name = Column(String(255), nullable=False)
    phone = Column(CHAR(10), nullable=False, unique=True)
    cnpj = Column(CHAR(14), nullable=False, unique=True)
    type = Column(Enum(ClinicType))
    address = Column(String(255), nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)

    validators = {
        "name": Validator("name").required().length(2, 255),
        "phone": Validator("phone").required().phone(),
        "cnpj": Validator("cnpj").required().cnpj(),
        "type": Validator("type").required().enum(ClinicType),
        "address": Validator("address").required(),
        "latitude": Validator("latitude").latitude(),
        "longitude": Validator("longitude").longitude(),
    }
