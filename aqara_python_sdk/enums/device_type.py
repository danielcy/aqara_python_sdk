from enum import Enum


class DeviceType(Enum):
    LIGHT = 0
    SWITCH = 1
    CURTAIN = 2
    UNSUPPORTED = -1
    ANY = -2
