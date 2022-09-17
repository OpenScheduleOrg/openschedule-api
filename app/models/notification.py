from sqlalchemy import Column, ForeignKey, String, Integer, Boolean
from sqlalchemy.orm import relationship

from . import db, TimestampMixin


class Notification(TimestampMixin, db.Model):
    """
    Hey not to see here
    """
    __tablename__ = "notification"

    message = Column(String(255))
    send = Column(Boolean, default=False)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
