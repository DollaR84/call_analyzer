from dataclasses import dataclass, field, asdict
from typing import Any


@dataclass(slots=True)
class BaseParamsData:
    max_tokens: int = 2000
    temperature: float = 0.1

    def to_dict(self, exclude_unset: bool = False, exclude: set[str] | None = None) -> dict[str, Any]:
        result = asdict(self)

        if exclude_unset:
            result = {key: value for key, value in result.items() if value is not None}

        if exclude:
            result = {key: value for key, value in result.items() if key not in exclude}

        return result


@dataclass(slots=True)
class GroqParamsData(BaseParamsData):
    presence_penalty: float = 0.0
    frequency_penalty: float = 0.0
    response_format: dict[str, str] = field(default_factory=lambda: {"type": "json_object"})
