import re

from .exceptions import APIException
from .constants import ValidationMessages


def useless_params(params, useful_parameters):
    """
        This method verify if the request parameters useless.
    """
    detail = {}
    for key in params:
        if key not in useful_parameters:
            detail[key] = "useless"

    if detail:
        raise APIException(ValidationMessages.PARAMETERS_USELESS,
                           detail=detail,
                           status_code=422)


def remove_mask(obj: str) -> str:
    """
    Remove everything that is not number
    """
    return re.sub(r"\D", "", obj)
