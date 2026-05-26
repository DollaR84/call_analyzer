from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type

from llm.types import LLMType

from .data import BaseParamsData


class BaseModel(ABC):
    _adapters: dict[str, Type[BaseModel]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)

        adapter_name = cls.get_name()
        if adapter_name not in cls._adapters:
            cls._adapters[adapter_name] = cls

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.replace("Model", "").lower()

    @classmethod
    def get(cls, name: LLMType, *args: Any, **kwargs: Any) -> BaseModel:
        model_cls = cls._adapters.get(name)
        if model_cls is None:
            raise ValueError(f"Model '{name}' does not exist")

        return model_cls(*args, **kwargs)

    def __init__(self, base_url: str, api_key: str, model: str):
        self.base_url = base_url
        self.api_key = api_key
        self.model = model

        self._params: BaseParamsData

    @property
    def params(self) -> dict[str, Any]:
        return self._params.to_dict()

    @abstractmethod
    def get_model_id(self) -> str:
        raise NotImplementedError
