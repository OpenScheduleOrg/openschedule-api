from app import db
from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship

class Consulta(db.Model):
    __tablename__ = "consulta"

    id = Column(Integer, primary_key=True, autoincrement=True)
    marcada = (DateTime)
    descricao = Column(String(255))
    realizada = Column(Boolean)
    id_cliente = Column(Integer, ForeignKey(
        'cliente.id'), nullable=False)
    id_clinica = Column(Integer, ForeignKey(
        'clinica.id'), nullable=False)

    cliente = relationship("Cliente", back_populates="consultas")
    clinica = relationship("Clinica", back_populates="consultas")

    def __init__(self, id_cliente, id_clinica, descricao, marcada, realizada=False):
        self.id_cliente = id_cliente
        self.id_clinica = id_clinica
        self.descricao = descircao
        self.marcada = marcada
        self.realizada = realizada

    def to_json(self):
        return {"id": self.id_consulta, "nome": self.cliente.nome,"marcada":self.marcada, "descricao":self.descricao, "realizada":self.realizada , "clinica": self.clinica.nome}


