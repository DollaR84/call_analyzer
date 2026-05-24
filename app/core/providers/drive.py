from typing import Optional

from dishka import Provider, Scope, provide

from core import Config
from drive import GoogleDriveClient, DriveServiceProtocol, GoogleDriveService, NullDriveService
from drive import DriveManager, ManagerData


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

    @provide(scope=Scope.APP)
    async def get_manager_data(self, config: Config) -> ManagerData:
        return ManagerData(
            audio_path=config.paths.audio_path,
            transcription_path=config.paths.transcription_path,
            folder_id=config.google.audio_folder or "",
            max_concurrent=config.google.max_concurrent,
        )

    @provide(scope=Scope.APP)
    async def get_manager(self, config: ManagerData, drive: DriveServiceProtocol) -> DriveManager:
        return DriveManager(config, drive)
