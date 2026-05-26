import asyncio
import logging
from pathlib import Path
from typing import Callable, Optional

from schemas import OutputFiles, Report, Transcript

from .data import FormatterContainer
from .writers import BaseWriter


logger = logging.getLogger(__name__)


class FormatterManager:

    def __init__(self, writers: FormatterContainer, max_concurrent: int = 5):
        self.writers = writers
        self.max_concurrent = max_concurrent

    def _safe_execute(self, func: Callable[[], Path], action_name: str, writer_name: str) -> Optional[Path]:
        try:
            return func()
        except OSError as e:
            logger.error("Error saving '%s' with formatter %s: %s", action_name, writer_name, e)
            return None

    def _sync_save(self, data: Transcript) -> OutputFiles:
        saved_paths = {}

        for name, writer in self.writers.items():
            def call_save(w: BaseWriter = writer) -> Path:
                return w.save(data)

            path = self._safe_execute(
                func=call_save,
                action_name=type(data).__name__,
                writer_name=name
            )

            if path is not None:
                saved_paths[name] = path

        return OutputFiles(**saved_paths)

    async def save(self, data: Transcript) -> OutputFiles:
        return await asyncio.to_thread(self._sync_save, data)

    async def report(self, report: Report) -> None:
        await asyncio.to_thread(
            self._safe_execute,
            lambda: self.writers.excel.save(report),
            type(report).__name__,
            self.writers.excel.get_name()
        )

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
