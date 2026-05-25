from __future__ import annotations

from abc import ABC, abstractmethod
import logging
from pathlib import Path
from typing import Any, Type

from schemas import Transcript


logger = logging.getLogger(__name__)


class BaseWriter(ABC):
    _adapters: dict[str, Type[BaseWriter]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        adapter_name = cls.get_name()
        if adapter_name not in cls._adapters:
            cls._adapters[adapter_name] = cls

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.replace("Writer", "").lower()

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def save(self, transcript: Transcript) -> Path:
        raise NotImplementedError
