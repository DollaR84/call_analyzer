import asyncio
import logging
from pathlib import Path

from .data import ManagerData
from .service import DriveServiceProtocol


logger = logging.getLogger(__name__)


class DriveManager:

    def __init__(self, config: ManagerData, drive: DriveServiceProtocol):
        self.config = config
        self.drive = drive

    async def run_sync(self) -> list[Path]:
        await self._sync_from_drive()

        queue = self._get_unprocessed_audio_files()
        logger.info("Found files to process: %d", len(queue))
        return queue

    async def _sync_from_drive(self) -> None:
        existing_local_names: set[str] = {file.name for file in self.config.audio_path.iterdir() if file.is_file()}
        cloud_files = await self.drive.list_files(self.config.folder_id)

        max_concurrent = self.config.max_concurrent
        semaphore = asyncio.Semaphore(max_concurrent)

        async def sem_download(file_id: str, destination: Path) -> None:
            async with semaphore:
                await self.drive.download_file(file_id, destination)

        download_tasks = []
        for file_info in cloud_files:
            if file_info.name in existing_local_names:
                continue

            logger.info("Scheduling download for new file: %s", file_info.name)
            destination = self.config.audio_path / file_info.name
            download_tasks.append(sem_download(file_info.id, destination))

        if download_tasks:
            logger.info("Starting download of %d files max concurrent %d...", len(download_tasks), max_concurrent)
            results = await asyncio.gather(*download_tasks, return_exceptions=True)

            for result in results:
                if isinstance(result, Exception):
                    logger.error("Error during file download: %s", str(result))

        else:
            logger.info("All cloud files are up to date. Nothing to download.")

    def _get_unprocessed_audio_files(self) -> list[Path]:
        existing_transcripts: set[str] = {
            file.stem for file in self.config.transcription_path.iterdir()
            if file.is_file()
        }

        unprocessed: list[Path] = []
        for audio_file in self.config.audio_path.iterdir():
            if audio_file.is_file() and not audio_file.name.startswith('.'):
                if audio_file.stem not in existing_transcripts:
                    unprocessed.append(audio_file)

        return unprocessed
