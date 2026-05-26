import asyncio
import logging
from pathlib import Path

from dishka import AsyncContainer

from core import Config
from drive import DriveManager
from formatters import FormatterManager
from diarization import DiarizationManager
from transcription import TranscriptionManager
from llm import LLMService
from schemas import OutputFiles


logger = logging.getLogger(__name__)


class ProcessingManager:

    def __init__(self, container: AsyncContainer):
        self.container = container

    async def _process_audio_to_text(
            self,
            audio_file: Path,
            transcripter: TranscriptionManager,
            diarizer: DiarizationManager,
            formatter: FormatterManager,
    ) -> OutputFiles:
        transcript = await transcripter.transcribe(audio_file)
        transcript = await diarizer.diarization(audio_file, transcript)
        files = await formatter.save(transcript)
        return files

    async def _process_analyze_text(
            self,
            files: OutputFiles,
            llm: LLMService,
            formatter: FormatterManager,
    ) -> OutputFiles:
        report = await llm.process(files)

        if report:
            await formatter.report(report)
        else:
            logger.warning("LLM analyze call '%s' failed!", files.json.stem)

        return files

    async def process(self) -> list[OutputFiles]:
        valid_results = []
        async with self.container as container:
            config = await container.get(Config)
            driver = await container.get(DriveManager)
            formatter = await container.get(FormatterManager)
            transcripter = await container.get(TranscriptionManager)
            diarizer = await container.get(DiarizationManager)
            llm = await container.get(LLMService)

            unprocessed = await driver.run_sync()
            semaphore = asyncio.Semaphore(config.ml.max_concurrent)

            async def sem_processing(audio_file: Path) -> OutputFiles:
                async with semaphore:
                    files = await self._process_audio_to_text(audio_file, transcripter, diarizer, formatter)
                    return await self._process_analyze_text(files, llm, formatter)

            tasks = [
                sem_processing(audio_file)
                for audio_file in unprocessed
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, BaseException):
                    logger.error("Error processing file: %s", result)
                else:
                    valid_results.append(result)

        logger.info("processed %d files", len(valid_results))
        return valid_results
