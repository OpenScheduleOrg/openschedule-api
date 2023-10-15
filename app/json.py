import json
from datetime import date

from flask.json.provider import DefaultJSONProvider

from app.models import ClinicType


def _custom_default(o):
    """
    custom default
    """
    if isinstance(o, ClinicType):
        return int(o.value)
    if isinstance(o, date):
        return o.isoformat()

    return DefaultJSONProvider.default(o)


class CustomJSONProvider(DefaultJSONProvider):
    default = staticmethod(_custom_default)

    def dumps(self, obj, **kwargs):
        kwargs.setdefault("default", self.default)
        kwargs.setdefault("ensure_ascii", self.ensure_ascii)
        kwargs.setdefault("sort_keys", self.sort_keys)
        return json.dumps(obj, **kwargs)
