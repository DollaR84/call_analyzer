import logging
from pathlib import Path
import time
from typing import Iterable

import ffmpeg
import numpy as np
from tqdm import tqdm

from faster_whisper import WhisperModel
from faster_whisper.transcribe import Segment, TranscriptionInfo

from core.types import Device

from .types import ComputeType, WhisperModelType


logger = logging.getLogger(__name__)


class WhisperClient:

    def __init__(self, model: WhisperModelType, device: Device, compute_type: ComputeType):
        start_time = time.time()

        with tqdm(total=0, bar_format="{desc}", desc="Loading Whisper model into memory... "):
            self.model = WhisperModel(
                model,
                device=device,
                compute_type=compute_type,
            )

        logger.info("Model loaded successfully in %.2f seconds!", time.time() - start_time)

    def _audio_to_numpy(self, path: str) -> np.ndarray:
        with tqdm(total=0, bar_format="{desc}", desc=f"Extracting audio track via FFmpeg: {Path(path).name}... "):
            try:
                out, _ = (
                    ffmpeg
                    .input(path)
                    .output("pipe:", format="f32le", acodec="pcm_f32le", ac=1, ar="16000")
                    .run(capture_stdout=True, capture_stderr=True)
                )
                return np.frombuffer(out, np.float32)
            except ffmpeg.Error as e:
                error_message = e.stderr.decode("utf-8") if e.stderr else str(e)
                raise RuntimeError(f"FFmpeg decoding failed for {path}: {error_message}") from e

    def transcribe(self, audio_source: str | np.ndarray) -> tuple[Iterable[Segment], TranscriptionInfo]:
        if isinstance(audio_source, str):
            audio_source = self._audio_to_numpy(audio_source)

        segments, info = self.model.transcribe(
            audio_source,
            task="transcribe",
            vad_filter=True,
            vad_parameters={
                "min_silence_duration_ms": 400,
                "speech_pad_ms": 400,
                "threshold": 0.4,
            },
            condition_on_previous_text=True,
            beam_size=5,
        )
        return segments, info
