import re
from datetime import date
from dateutil.parser import isoparse

from sqlalchemy import Column, Date, String
from sqlalchemy.orm import relationship, validates

from . import session, select, db, TimestampMixin
from ..exceptions import APIExceptionHandler


class Cliente(TimestampMixin, db.Model):
    __tablename__ = "cliente"
    nome = Column(String(255), nullable=False)
    sobrenome = Column(String(255), nullable=False, default="")
    cpf = Column(String(11), nullable=False)
    telefone = Column(String(10), nullable=False)
    endereco = Column(String(255), default=None)
    nascimento = Column(Date, default=None)

    consultas = relationship("Consulta", back_populates="cliente")

    def as_json(self):
        """
            Model to json
        """
        obj_json = super().as_json()

        del obj_json["created_at"]
        del obj_json["updated_at"]

        return obj_json

    @validates("cpf")
    def validate_cpf(self, key, cpf):
        """
        validate cpf format
        """
        cpf = cpf.replace(".", "").replace("-", "")
        if re.match(r"^\d{11}$", cpf):
            res = session.execute(
                select(Cliente).where(Cliente.cpf == cpf,
                                      Cliente.id != self.id)).scalar()
            if res:
                raise APIExceptionHandler("O cpf já foi cadastrado.",
                                          detail={key: "registered"})
            return cpf

        raise APIExceptionHandler("Invalid format cpf.",
                                  detail={key: "invalid"})

    @validates("telefone")
    def validate_telefone(self, key, telefone):
        """
        Validate fone format
        """
        telefone = re.sub(r"\s+|-+|\(|\)|\+", "", telefone)

        if (re.match(r"^\d{11}$", telefone) and telefone[-9] == "9"):
            telefone = telefone[0:2] + telefone[3:]
        if re.match(r"^\d{10}$", telefone):
            res = session.execute(
                select(Cliente).where(Cliente.telefone == telefone,
                                      Cliente.id != self.id)).scalar()
            if res:
                raise APIExceptionHandler("O telefone já foi cadastrado.",
                                          detail={key: "registered"})
            return telefone

        raise APIExceptionHandler("Telefone invlalid.",
                                  detail={key: "invalid"})

    @validates("nascimento")
    def validate_nascimento(self, key, nascimento):
        """
        validate birth date
        """
        if not isinstance(nascimento, date):
            try:
                nascimento = isoparse(nascimento).date()
            except ValueError as error:
                raise APIExceptionHandler("Data de nascimento invalid.",
                                          detail={key: "invalid"}) from error
            except Exception as error:
                raise error

        return nascimento
