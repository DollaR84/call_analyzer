from enum import StrEnum


class Device(StrEnum):
    CPU = "cpu"
    CUDA = "cuda"
    AUTO = "auto"
