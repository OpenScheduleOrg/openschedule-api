from decimal import Decimal

from faker import Faker

from app.models import Clinic, ClinicType

fake = Faker(["pt_BR"])


class ClinicBuilder():

    def __init__(self):
        self.clinic = {
            "name":
            fake.company(),
            "phone":
            fake.msisdn()[-10:],
            "cnpj":
            fake.company_id(),
            "type":
            fake.random_element([
                ClinicType.PEDIATRIC, ClinicType.DENTISTRY,
                ClinicType.OCCUPATIONAL
            ]),
            "address":
            fake.address(),
        }

    def with_name(self, value: str):
        """
        Set a name to build
        """
        self.clinic["name"] = value
        return self

    def with_phone(self, value: str):
        """
        Set a phone to build
        """
        self.clinic["phone"] = value
        return self

    def with_type(self, value: ClinicType):
        """
        Set a type to build
        """
        self.clinic["type"] = value
        return self

    def with_cnpj(self, value: str):
        """
        Set a cnpj to build
        """
        self.clinic["cnpj"] = value
        return self

    def with_address(self, value: str):
        """
        Set a address to build
        """
        self.clinic["address"] = value
        return self

    def with_latitude(self, value: Decimal):
        """
        Set a latitude to build
        """
        self.clinic["latitude"] = value
        return self

    def with_longitude(self, value: Decimal):
        """
        Set a longitude to build
        """
        self.clinic["longitude"] = value
        return self

    def complete(self):
        """
        Complete with field no required
        """
        latlng = fake.latlng()
        self.clinic["latitude"] = float(latlng[0])
        self.clinic["longitude"] = float(latlng[1])
        return self

    def build(self):
        """
        Build clinic
        """
        return self.clinic

    def build_object(self):
        """
        Build clinic as object
        """
        return Clinic(**self.clinic)
