import re
from enum import Enum
from datetime import date
from dateutil.parser import isoparse

from .exceptions import ValidationException
from .constants import ValidationMessages
from .utils import remove_mask


def validate_cpf(field: str, body: dict) -> str or None:
    """
    Validate cpf
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    cpf = body[field] = remove_mask(body[field])
    if re.match(r"^\d{11}$", cpf):
        digits = [int(d) for d in cpf]
        dvs = [0, 0]

        for i in range(11, 2, -1):
            dvs[0] += digits[11 - i] * (i - 1)
            dvs[1] += digits[11 - i] * i

        dvs[0] = ((11 - (dvs[0] % 11)) % 11) % 10
        dvs[1] = ((11 - ((dvs[1] + (dvs[0] * 2)) % 11)) % 11) % 10

        if dvs[0] == digits[9] and dvs[1] == digits[10]:
            return None
    return ValidationMessages.INVALID_CPF.format(field)


def validate_cnpj(field: str, body: dict) -> str or None:
    """
    Validate cnpj
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    cnpj = body[field] = remove_mask(body[field])
    if re.match(r"^\d{14}$", cnpj):
        digits = [int(d) for d in cnpj]
        dvs = [0, 0]

        i = 6
        j = 5
        for d in digits[:-2]:
            dvs[0] += i * d
            dvs[1] += j * d
            i += 1 if i < 9 else -7
            j += 1 if j < 9 else -7

        dvs[0] = (dvs[0] % 11) % 10
        dvs[1] = ((dvs[1] + dvs[0] * 9) % 11) % 10

        if dvs[0] == digits[12] and dvs[1] == digits[13]:
            return None
    return ValidationMessages.INVALID_CNPJ.format(field)


def validate_phone(field: str, body: dict) -> str or None:
    """
    Validate phone
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    phone = remove_mask(body[field])
    if (re.match(r"^\d{11}$", phone) and phone[-9] == "9"):
        phone = phone[0:2] + phone[3:]
    if re.match(r"^\d{10}$", phone):
        body[field] = phone
        return None

    return ValidationMessages.INVALID_PHONE.format(field)


def validate_email(field: str, body: dict) -> str or None:
    """
    Validate email
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    # pylint: disable=line-too-long
    if re.match(
            r"^(([^<>()[\]\\.,;:\s@\"]+(\.[^<>()[\]\\.,;:\s@\"]+)*)|(\".+\"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$",
            body[field]):
        return None

    return ValidationMessages.INVALID_EMAIL


def validate_required(field: str, body: dict):
    """
    Validate if fields are in payload
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    return ValidationMessages.REQUIRED_FIELD.format(
        field) if field not in body or body[field] is None else None


def validate_number(field: str, body: dict):
    """
    Validate if field is a number
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    if not isinstance(body[field], date):
        try:
            body[field] = int(body[field])
        except ValueError:
            return ValidationMessages.NOT_A_NUMBER.format(field)
    return None


def validate_date(field: str, body: dict):
    """
    Validate if field is a date
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    if not isinstance(body[field], date):
        try:
            body[field] = isoparse(body[field]).date()
        except ValueError:
            return ValidationMessages.INVALID_DATE.format(field)
    return None


def validate_range(field: str, body: dict, min_value: int, max_value: int):
    """
    Validate if field is in range
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
            min_value (int): minimum value in range inclusive
            max_value (int): maximum value in range inclusive
        returns:
            validation message if invalid or none if valid
    """
    value = body[field]
    if value < min_value or value > max_value:
        return ValidationMessages.OUT_OF_RANGE.format(min_value, max_value)
    return None


def validate_length(field: str, body: dict, min_len=None, max_len=None):
    """
    Validate field string length
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
            min_len (int): minimum characters expected
            max_len (int): maximum characters expected
        returns:
            validation message if invalid or none if valid
    """
    if min_len is None and max_len is None:
        raise ValueError("At least min or max must have some value.")

    length = len(body[field])

    if min_len is not None and length < min_len:
        return ValidationMessages.LEAST_CHARACTERS.format(field, min_len)

    if max_len is not None and length > max_len:
        return ValidationMessages.MOST_CHARACTERS.format(field, max_len)

    return None


def validate_enum(field: str, body: dict, enum: Enum):
    """
    Validate if field is a longitude
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
            enum (Enum): type of enum to validate
        returns:
            validation message if invalid or none if valid
    """
    try:
        body[field] = enum(body[field])
    except ValueError:
        return ValidationMessages.NOT_IN_ENUM.format(body[field],
                                                     enum.__qualname__)

    return None


class Validator:

    def __init__(self, field):
        self.field = field
        self.validators = []
        self.nullable = True

    def required(self):
        """
        Add validate required to validators
        """
        self.nullable = False
        self.validators.append(validate_required)
        return self

    def cpf(self):
        """
        Add validate cpf to validators
        """
        self.validators.append(validate_cpf)
        return self

    def cnpj(self):
        """
        Add validate cnpj to validators
        """
        self.validators.append(validate_cnpj)
        return self

    def phone(self):
        """
        Add validate phone to validators
        """
        self.validators.append(validate_phone)
        return self

    def email(self):
        """
        Add validate email to validators
        """
        self.validators.append(validate_email)
        return self

    def number(self):
        """
        Add validate number to validators
        """
        self.validators.append(validate_number)
        return self

    def date(self):
        """
        Add validate date to validators
        """
        self.validators.append(validate_date)
        return self

    def range(self, min_value, max_value):
        """
        Add validate range to validators
        """
        self.validators.append(
            lambda f, b: validate_range(f, b, min_value, max_value))
        return self

    def length(self, min_len=None, max_len=None):
        """
        Add validate length to validators
        """
        self.validators.append(
            lambda f, b: validate_length(f, b, min_len, max_len))
        return self

    def enum(self, enum: Enum):
        """
        Add validate enum to validators
        """
        self.validators.append(lambda f, b: validate_enum(f, b, enum))
        return self

    def validate(self, obj: dict) -> str or None:
        """
        Validate field with validators
        """
        if not (self.nullable and
                (self.field not in obj or obj[self.field] is None)):
            for validator in self.validators:
                if result := validator(self.field, obj):
                    return result
        return None


def validate_payload(payload: dict,
                     validators: dict[str, Validator],
                     fields: list[str] = None):
    """
    Validate fields of payload with validators
    """
    errors = {}
    for field in fields or validators:
        result = validators[field].validate(payload)
        if result:
            errors[field] = result
    if errors:
        raise ValidationException(errors)
