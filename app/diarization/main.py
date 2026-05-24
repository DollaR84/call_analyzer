import asyncio
import logging
from pathlib import Path

from schemas import Transcript

from .service import DiarizationService


logger = logging.getLogger(__name__)


class DiarizationManager:

    def __init__(self, service: DiarizationService, max_concurrent: int = 3):
        self.service = service
        self.max_concurrent = max_concurrent

    async def diarization(self, audio_path: Path, data: Transcript) -> Transcript:
        return await self.service.diarization(audio_path, data)

    async def process(self, audio_files: list[Path], transcripts: list[Transcript]) -> list[Transcript]:
        transcript_map = {t.file_name: t for t in transcripts}
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_diarization(audio_file: Path, data: Transcript) -> Transcript:
            async with semaphore:
                return await self.diarization(audio_file, data)

        tasks = []
        for audio_file in audio_files:
            data = transcript_map.get(audio_file.stem)
            if not data:
                logger.warning("no transcription data found for file: %s", audio_file.name)
                continue

            tasks.append(sem_diarization(audio_file, data))
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for result in results:
            if isinstance(result, BaseException):
                logger.error("Error diarization file: %s", result)
            else:
                valid_results.append(result)

        return valid_results
