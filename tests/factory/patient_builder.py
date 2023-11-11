from datetime import datetime

from faker import Faker

from app.models import Patient

fake = Faker(["pt_BR"])


class PatientBuilder():

    def __init__(self):
        self.patient = {
            "name": fake.company(),
            "cpf": fake.ssn(),
            "registration": fake.pystr_format("####?2???####"),
            "phone": fake.msisdn()[-10:],
        }

    def with_name(self, value: str):
        """
        Set a name to build
        """
        self.patient["name"] = value
        return self

    def with_phone(self, value: str):
        """
        Set a phone to build
        """
        self.patient["phone"] = value
        return self

    def with_cpf(self, value: str):
        """
        Set a cpf to build
        """
        self.patient["cpf"] = value
        return self

    def with_registration(self, value: str):
        """
        Set a cpf to build
        """
        self.patient["registration"] = value
        return self

    def with_address(self, value: str):
        """
        Set a address to build
        """
        self.patient["address"] = value
        return self

    def with_birthdate(self, value: datetime):
        """
        Set a birthdate to build
        """
        self.patient["birthdate"] = value
        return self

    def complete(self):
        """
        Complete with field no required
        """
        self.patient["address"] = fake.address()
        self.patient["birthdate"] = fake.date_of_birth()
        return self

    def build(self):
        """
        Build patient
        """
        if "birthdate" in self.patient:
            try:
                self.patient["birthdate"] = self.patient[
                    "birthdate"].isoformat()
            except AttributeError:
                pass

        return self.patient

    def build_object(self):
        """
        Build patient as object
        """
        return Patient(**self.patient)
