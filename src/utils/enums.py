from enum import Enum, IntEnum


class Axis(Enum):
    X = 1
    Y = 2


class ResolutionLevel(IntEnum):
    LEVEL_0_BASE = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3
    THUMBNAIL = 4
