import asyncio
import logging

from schemas import OutputFiles, Transcript

from .json import JsonWriter
from .txt import TxtWriter


logger = logging.getLogger(__name__)


class FormatterManager:

    def __init__(self, json_writer: JsonWriter, txt_writer: TxtWriter, max_concurrent: int = 5):
        self.json_writer = json_writer
        self.txt_writer = txt_writer
        self.max_concurrent = max_concurrent

    def _sync_save(self, data: Transcript) -> OutputFiles:
        json_path = self.json_writer.save(data)
        txt_path = self.txt_writer.save(data)
        return OutputFiles(json=json_path, txt=txt_path)

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
