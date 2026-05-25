from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass(frozen=True, slots=True)
class OutputFiles:
    json: Path
    txt: Path

    excel: Optional[Path] = None
