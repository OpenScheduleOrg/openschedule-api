from sqlalchemy import Integer, Column, ForeignKey

from . import db, TimestampMixin


class Acting(TimestampMixin, db.Model):

    __tablename__ = "actuations"

    professional_id = Column(Integer,
                             ForeignKey('professionals.id'),
                             nullable=False)
    specialty_id = Column(Integer,
                          ForeignKey('specialties.id'),
                          nullable=False)
    clinic_id = Column(Integer, ForeignKey('clinics.id'), nullable=False)
