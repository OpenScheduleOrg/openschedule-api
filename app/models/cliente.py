from app import db
from sqlalchemy import Column, ForeignKey, Integer, Date, Time, String, DateTime, Boolean
from sqlalchemy.orm import relationship



class Cliente(db.Model):
    __tablename__ = "cliente"
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    cpf = Column(String(14), nullable=False)
    telefone = Column(String(20), nullable=False)
    endereco = Column(String(255), default=None)
    nascimento = Column(Date, default=None)

    consultas = relationship("Consulta", back_populates="cliente")
    def __init__(self,  nome, cpf, telefone, endereco, nascimento):
        self.nome = nome
        self.cpf = cpf
        self.telefone = telefone
        self.endereco = endereco
        self.nascimento = nascimento

    def to_json(self):
        return {"id": self.id_cliente, "nome": self.nome, "cpf": self.cpf, "telefone": self.telefone, "endereco": self.endereco, "nascimento":self.nascimento}


