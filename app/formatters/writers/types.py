from enum import IntEnum


class ExcelRows(IntEnum):
    HEADER = 2


class ExcelColumns(IntEnum):
    DATE = 1
    TRANSCRIPT = 12

    REQUESTED_WORK = 14
    MANAGER_SCORE = 18
    COMMENT = 20

    PROPER_GREETING = 6
    KNOWS_BODY_TYPE = 7
    KNOWS_YEAR = 8
    KNOWS_MILEAGE = 9
    OFFERED_COMPLEX_DIAGNOSTICS = 10
    KNOWS_HISTORY = 11
    PROPER_GOODBYE = 13
    FOLLOWED_TOP_100_RULES = 15
