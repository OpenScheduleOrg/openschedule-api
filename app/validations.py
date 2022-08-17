import re
from datetime import date
from dateutil.parser import isoparse

from sqlalchemy.exc import IntegrityError
from .exceptions import APIException, ValidationException
from .constants import ValidationMessages
from .utils import remove_mask


def validate_dates(**kw):
    """
        This method verify if the date parameters are valids.
    """
    detail = {}
    converted = []
    keys = []

    for key, value in kw.items():
        keys.append(key)
        try:
            converted.append(isoparse(value))
        except (ValueError, TypeError):
            detail[key] = "invalid"
        except Exception as error:
            raise error

    if detail:
        raise APIException("Date and time are not in iso format",
                           detail=detail)

    if ((isinstance(converted[0], date) and isinstance(converted[1], date))
            and converted[0] > converted[1]):
        raise APIException("Invalid datetime values date_start < date_end",
                           detail={
                               keys[0]: "invalid",
                               keys[1]: "invalid"
                           })

    return converted


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


def validate_phone(field: str, body: dict) -> str or None:
    """
    Validate cpf
        parameters:
            field (str): field to validate
            body (dict): object with field to validate
        returns:
            validation message if invalid or none if valid
    """
    phone = body[field] = remove_mask(body[field])
    if (re.match(r"^\d{11}$", phone) and phone[-9] == "9"):
        phone = phone[0:2] + phone[3:]
    if re.match(r"^\d{10}$", phone):
        return None
    return ValidationMessages.INVALID_PHONE.format(field)


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

    def phone(self):
        """
        Add validate phone to validators
        """
        self.validators.append(validate_phone)
        return self

    def date(self):
        """
        Add validate date to validators
        """
        self.validators.append(validate_date)
        return self

    def length(self, min_len=None, max_len=None):
        """
        Add validate cnpj to validators
        """
        self.validators.append(
            lambda f, b: validate_length(f, b, min_len, max_len))
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


def validate_unique(error: IntegrityError, fields_message: dict):
    """
    Validate if field already registered with database error unique constraint
    """
    db_error_msg = error.orig.args and error.orig.args[0][::-1]
    field = ""
    if "EUQINU" in db_error_msg:
        for c in db_error_msg:
            if c == ".":
                break
            field = c + field
        if field in fields_message:
            raise ValidationException({field: fields_message[field]})
