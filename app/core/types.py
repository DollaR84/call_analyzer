from enum import StrEnum


class DeviceType(StrEnum):
    CPU = "cpu"
    CUDA = "cuda"
    AUTO = "auto"
