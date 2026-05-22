from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from transcription.types import ComputeType, WhisperDevice, WhisperModel
from utils.google import extract_folder_id


class PathConfig(BaseModel):
    data_dir: Path = Path("data")
    audio_subdir: Path = Path("audio")
    reports_subdir: Path = Path("reports")
    transcripts_subdir: Path = Path("transcripts")

    @property
    def audio_path(self) -> Path:
        return self.data_dir / self.audio_subdir

    @property
    def reports_path(self) -> Path:
        return self.data_dir / self.reports_subdir

    @property
    def transcription_path(self) -> Path:
        return self.data_dir / self.transcripts_subdir


class WhisperConfig(BaseModel):
    compute_type: ComputeType
    device: WhisperDevice
    model: WhisperModel
    max_concurrent: int = 3


class GoogleConfig(BaseModel):
    credentials_path: Optional[Path] = None
    audio_folder: Optional[str] = None

    max_concurrent_downloads: int = 1
    max_retries: int = 5

    @field_validator("audio_folder")
    @classmethod
    def clean_folder_id(cls, value: Optional[str]) -> Optional[str]:
        if value is None or value.strip() == "":
            return None

        return extract_folder_id(value)

    @property
    def is_audio_access(self) -> bool:
        return bool(self.credentials_path and self.audio_folder)


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    whisper: WhisperConfig
    paths: PathConfig = Field(default_factory=PathConfig)
    google: GoogleConfig = Field(default_factory=GoogleConfig)


@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config()
