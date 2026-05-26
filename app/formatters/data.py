from dataclasses import dataclass, fields
from typing import Iterator

from .writers import (
    BaseWriter,
    ExcelWriter,
    JsonWriter,
    TxtWriter,
)


@dataclass(frozen=True, slots=True)
class FormatterContainer:
    excel: ExcelWriter
    json: JsonWriter
    txt: TxtWriter

    def __iter__(self) -> Iterator[BaseWriter]:
        return iter((self.excel, self.json, self.txt))

    def items(self) -> Iterator[tuple[str, BaseWriter]]:
        for field in fields(self):
            yield field.name, getattr(self, field.name)
