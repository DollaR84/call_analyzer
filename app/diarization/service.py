import asyncio
import logging
from pathlib import Path
import time

from tqdm import tqdm

from schemas import Transcript

from .client import DiarizationClient


logger = logging.getLogger(__name__)


class DiarizationService:

    def __init__(self, client: DiarizationClient):
        self.client = client

    def _sync_diarization(self, audio_path: Path, data: Transcript) -> Transcript:
        start_time = time.time()
        with tqdm(total=0, bar_format="{desc}", desc=f"processing diarization file: {data.file_name}... "):
            data.segments = self.client.diarization(
                str(audio_path),
                data.segments,
            )

        logger.info("diarization file successfully in %.2f seconds!", time.time() - start_time)
        return data

    async def diarization(self, audio_path: Path, data: Transcript) -> Transcript:
        data = await asyncio.to_thread(
            self._sync_diarization,
            audio_path,
            data
        )

        return data
