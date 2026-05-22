from dishka import Provider, Scope, provide

from drive import DriveServiceProtocol
from manager import ManagerData, ProcessingManager

from ..config import Config, get_config


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        return get_config()

    @provide(scope=Scope.APP)
    async def get_manager_data(self, config: Config) -> ManagerData:
        return ManagerData(
            audio_path=config.paths.audio_path,
            transcription_path=config.paths.transcription_path,
            folder_id=config.google.audio_folder or "",
            max_concurrent=config.google.max_concurrent_downloads,
        )

    @provide(scope=Scope.APP)
    async def get_manager(self, config: ManagerData, drive: DriveServiceProtocol) -> ProcessingManager:
        return ProcessingManager(config, drive)
