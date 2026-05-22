import io
import logging
from pathlib import Path
import random
import socket
import ssl
import time
from typing import Any, Protocol

from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload
from google.oauth2.service_account import Credentials

from tqdm import tqdm

from .data import DriveFileResponse, DriveListResponse


logger = logging.getLogger(__name__)


class FilesResource(Protocol):

    def list(self, **kwargs: Any) -> Any:
        ...

    def get(self, **kwargs: Any) -> Any:
        ...

    def get_media(self, **kwargs: Any) -> Any:
        ...


class DriveFiles:

    def __init__(self, resource: Any):
        self._resource = resource

    def list(self, **kwargs: Any) -> Any:
        return self._resource.list(**kwargs)

    def get(self, **kwargs: Any) -> Any:
        return self._resource.get(**kwargs)

    def get_media(self, **kwargs: Any) -> Any:
        return self._resource.get_media(**kwargs)


class GoogleDriveClient:

    def __init__(self, credentials_path: Path, max_retries: int = 5):
        self.max_retries = max_retries
        scopes: list[str] = [
            "https://www.googleapis.com/auth/drive.readonly"
        ]

        creds: Credentials = Credentials.from_service_account_file(
            credentials_path,
            scopes=scopes
        )

        self.service: Resource = build("drive", "v3", credentials=creds, http=None, cache_discovery=False)
        self.files = DriveFiles(self.service.files())  # pylint: disable=no-member

    def list_files(self, folder_id: str) -> list[DriveFileResponse]:
        query: str = f"'{folder_id}' in parents and trashed = false"

        results: DriveListResponse = self.files.list(
            q=query,
            fields="files(id, name, mimeType)"
        ).execute()

        return results.get("files", [])

    def download_file(self, file_id: str, output_path: Path) -> None:
        file_metadata = self.files.get(fileId=file_id, fields="size").execute()
        file_size = int(file_metadata.get("size", 0))

        for attempt in range(self.max_retries):
            try:
                output_path.unlink(missing_ok=True)
                return self._downloader(file_id, output_path, file_size)

            except (HttpError, OSError, TimeoutError, socket.timeout, ssl.SSLError) as e:
                wait = min(2 ** attempt + random.random(), 30)

                logger.warning(
                    "[Drive] download failed (attempt %d/%d): %s",
                    attempt + 1,
                    self.max_retries,
                    e,
                    exc_info=True
                )
                logger.warning("[Drive] retrying in %.1f seconds...", wait)

                time.sleep(wait)
        raise RuntimeError(f"Failed to download file {file_id} after {self.max_retries} attempts")

    def _downloader(self, file_id: str, output_path: Path, file_size: int) -> None:
        request = self.files.get_media(fileId=file_id)

        with io.FileIO(output_path, "wb") as fh:
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)
            done = False

            with tqdm(
                total=file_size,
                disable=file_size <= 0,
                unit="B",
                unit_scale=True,
                desc=f"Downloading file {output_path.name} from Google Drive"
            ) as pbar:
                while not done:
                    status, done = downloader.next_chunk()
                    if status:
                        pbar.update(status.resumable_progress - pbar.n)
