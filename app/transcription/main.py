import asyncio
import logging
from pathlib import Path

from schemas import Transcript

from .service import TranscriptionService


logger = logging.getLogger(__name__)


class TranscriptionManager:

    def __init__(self, service: TranscriptionService, max_concurrent: int = 3):
        self.service = service
        self.max_concurrent = max_concurrent

    async def transcribe(self, audio_path: Path) -> Transcript:
        return await self.service.transcribe(audio_path)

    async def process(self, unprocessed: list[Path]) -> list[Transcript]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_transcribe(audio_file: Path) -> Transcript:
            async with semaphore:
                return await self.transcribe(audio_file)

        tasks = [
            sem_transcribe(audio_file)
            for audio_file in unprocessed
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for result in results:
            if isinstance(result, BaseException):
                logger.error("Error transcribe file: %s", result)
            else:
                valid_results.append(result)

        return valid_results
