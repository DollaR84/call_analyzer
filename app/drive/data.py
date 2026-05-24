from dataclasses import dataclass
from pathlib import Path
from typing import TypedDict


class DriveFileResponse(TypedDict):
    id: str
    name: str
    mimeType: str


class DriveListResponse(TypedDict, total=False):
    files: list[DriveFileResponse]


@dataclass(frozen=True, slots=True)
class ManagerData:
    audio_path: Path
    transcription_path: Path
    folder_id: str = ""
    max_concurrent: int = 1
