from typing import Optional

from dishka import Provider, Scope, provide

from core import Config
from drive import GoogleDriveClient, DriveServiceProtocol, GoogleDriveService, NullDriveService


class DriveProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_google_drive_client(self, config: Config) -> Optional[GoogleDriveClient]:
        if not config.google.is_audio_access or config.google.credentials_path is None:
            return None
        return GoogleDriveClient(config.google.credentials_path, max_retries=config.google.max_retries)

    @provide(scope=Scope.APP)
    async def get_drive_service(self, client: Optional[GoogleDriveClient]) -> DriveServiceProtocol:
        if client is None:
            return NullDriveService()
        return GoogleDriveService(client)
