import asyncio
import logging
from pathlib import Path

from .service import TranscriptionService
from .schemas import TranscriptResult
from .writer import TranscriptWriter


logger = logging.getLogger(__name__)


class Transcriber:

    def __init__(self, service: TranscriptionService, writer: TranscriptWriter, max_concurrent: int = 3):
        self.service = service
        self.writer = writer
        self.max_concurrent = max_concurrent

    async def transcribe(self, audio_path: Path) -> TranscriptResult:
        return await self.service.transcribe(audio_path)

    async def process(self, unprocessed: list[Path]) -> None:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_transcribe(audio_file: Path) -> None:
            async with semaphore:
                result = await self.transcribe(audio_file)
                self.writer.save(result)

        tasks = [
            sem_transcribe(audio_file)
            for audio_file in unprocessed
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        for result in results:
            if isinstance(result, Exception):
                logger.error("Error transcribe file: %s", str(result))
