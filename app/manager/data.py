from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True, slots=True)
class ManagerData:
    audio_path: Path
    transcription_path: Path
    folder_id: str = ""
    max_concurrent: int = 5
