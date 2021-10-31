from app import db
from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship


class Clinica(db.Model):
    __tablename__ = "clinica"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    tipo = Column(String(255))
    fone_contato = Column(String(20), nullable=False)
    endereco = Column(String(255), nullable=False)
    longitude = Column(String(45), nullable=False)
    latitude = Column(String(45), nullable=False)

    consultas = relationship("Consulta", back_populates="clinica")
    horarios = relationship("Horario", back_populates="clinica")

    def __init__(self, nome, tipo, fone_contato, endereco, longitude, latitude):
        self.nome = nome
        self.tipo = tipo
        self.fone_contato = fone_contato
        self.endereco = endereco
        self.long = longitude
        self.latitude = latitude

    def to_json(self):
        return {"id": self.id_clinica, "nome": self.nome, "tipo": self.tipo,
                "fone_contato": self.fone_contato, "endereco": {
                    "text": self.endereco,
                    "coord": {
                        "latitude": self.latitude,
                        "longitude": self.longitude
                    }
                }
                }


