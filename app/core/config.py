from functools import lru_cache
import os
from pathlib import Path
from typing import Optional

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.types import DeviceType
from llm.types import LLMType
from transcription.types import ComputeType, WhisperModelType
from utils.google import extract_folder_id


class PathConfig(BaseModel):
    data_dir: Path = Path("data")
    audio_subdir: Path = Path("audio")
    transcripts_subdir: Path = Path("transcripts")

    prompts_subdir: Path = Path("prompts")
    prompt_system: Path = Path("system")
    prompt_detail: Path = Path("detail")

    max_concurrent: int = 5

    @property
    def audio_path(self) -> Path:
        return self.data_dir / self.audio_subdir

    @property
    def transcription_path(self) -> Path:
        return self.data_dir / self.transcripts_subdir

    @property
    def prompts_path(self) -> Path:
        return self.data_dir / self.prompts_subdir

    @property
    def prompt_system_file(self) -> Path:
        return self.prompts_path / self.prompt_system

    @property
    def prompt_detail_file(self) -> Path:
        return self.prompts_path / self.prompt_detail


class MLConfig(BaseModel):
    device: DeviceType
    hf_token: Optional[str] = None
    max_concurrent: int = 3


class WhisperConfig(BaseModel):
    compute_type: ComputeType
    model: WhisperModelType


class GoogleConfig(BaseModel):
    credentials_path: Optional[Path] = None
    audio_folder: Optional[str] = None

    max_concurrent: int = 1
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


class LlmConfig(BaseModel):
    name: LLMType

    base_url: str
    api_key: str
    model: str


class Config(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_nested_delimiter="__")

    ml: MLConfig
    whisper: WhisperConfig
    llm: LlmConfig
    paths: PathConfig = Field(default_factory=PathConfig)
    google: GoogleConfig = Field(default_factory=GoogleConfig)


@lru_cache(maxsize=1)
def get_config() -> Config:
    config = Config()

    if config.ml.hf_token:
        os.environ["HF_TOKEN"] = config.ml.hf_token
        os.environ["HUGGINGFACE_HUB_TOKEN"] = config.ml.hf_token

    return config
