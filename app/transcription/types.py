from enum import StrEnum


class ComputeType(StrEnum):
    INT8 = "int8"
    FLOAT16 = "float16"
    FLOAT32 = "float32"


class WhisperModelType(StrEnum):
    TINY = "tiny"
    BASE = "base"
    SMALL = "small"

    MEDIUM = "medium"

    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"

    DISTIL_LARGE_V2 = "distil-large-v2"
    DISTIL_LARGE_V3 = "distil-large-v3"
