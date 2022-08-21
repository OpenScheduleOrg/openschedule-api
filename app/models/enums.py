from enum import Enum, unique


@unique
class ClinicType(Enum):
    __qualname__ = "type of clinic"

    PEDIATRIC = 0o0000_0002
    OCCUPATIONAL = 0o0000_0004
    DENTISTRY = 0o4000_0000
