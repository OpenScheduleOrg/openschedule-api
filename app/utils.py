from datetime import date
from dateutil.parser import isoparse

from .exceptions import APIExceptionHandler

def useless_params(params, useful_parameters):
    detail = {}
    for  key in params:
        if key not in useful_parameters:
            detail[key] = "unusable"

    if detail:
        raise APIExceptionHandler("Request have parameters worthless.", detail=detail, status_code=422)


def valid_date_params(**kw):
    detail = {}
    converted = []
    keys = []

    for key, value in kw.items():
        keys.append(key)
        if(value is None):
            converted.append(None)
            continue
        try:
            converted.append(isoparse(value))
        except ValueError as e:
            detail[key] = "invalid"
        except Exception as e:
            raise e

    if detail:
        raise APIExceptionHandler("Date and time are not in iso format", detail=detail)

    if((isinstance(converted[0], date) and isinstance(converted[1], date)) and converted[0] > converted[1]):
            raise APIExceptionHandler("Invalid datetime values date_start < date_end", detail={keys[0]: "invalid", keys[1]:"invalid"})

    return converted



