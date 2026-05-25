import asyncio
import logging

from schemas import OutputFiles, Transcript

from .writers import BaseWriter


logger = logging.getLogger(__name__)


class FormatterManager:

    def __init__(self, writers: list[BaseWriter], max_concurrent: int = 5):
        self.writers = writers
        self.max_concurrent = max_concurrent

    def _sync_save(self, data: Transcript) -> OutputFiles:
        saved_paths = {}

        for writer in self.writers:
            name = writer.get_name()
            try:
                path = writer.save(data)
                saved_paths[name] = path
            except OSError as e:
                logger.error("Error saving with formatter %s: %s", name, e)

        return OutputFiles(**saved_paths)

    async def save(self, data: Transcript) -> OutputFiles:
        return await asyncio.to_thread(self._sync_save, data)

    async def process(self, transcripts: list[Transcript]) -> list[OutputFiles]:
        semaphore = asyncio.Semaphore(self.max_concurrent)

        async def sem_save(data: Transcript) -> OutputFiles:
            async with semaphore:
                return await self.save(data)

        tasks = [
            sem_save(data)
            for data in transcripts
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        valid_results = []
        for result in results:
            if isinstance(result, BaseException):
                logger.error("Error save file: %s", result)
            else:
                valid_results.append(result)

        return valid_results
