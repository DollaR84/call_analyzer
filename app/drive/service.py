import asyncio
from pathlib import Path
from typing import Protocol

from schemas import DriveFile

from .client import GoogleDriveClient


class DriveServiceProtocol(Protocol):

    async def list_files(self, folder_id: str) -> list[DriveFile]:
        ...

    async def download_file(self, file_id: str, output_path: Path) -> None:
        ...


class NullDriveService:

    async def list_files(self, _: str) -> list[DriveFile]:
        return []

    async def download_file(self, file_id: str, output_path: Path) -> None:
        pass


class GoogleDriveService:

    def __init__(self, client: GoogleDriveClient):
        self.client = client

    async def list_files(self, folder_id: str) -> list[DriveFile]:
        files = await asyncio.to_thread(
            self.client.list_files,
            folder_id
        )

        return [
            DriveFile(**file)
            for file in files
        ]

    async def download_file(self, file_id: str, output_path: Path) -> None:
        output_path.parent.mkdir(parents=True, exist_ok=True)

        await asyncio.to_thread(
            self.client.download_file,
            file_id,
            output_path
        )
