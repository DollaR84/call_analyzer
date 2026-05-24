from collections.abc import AsyncIterator
import gc
import logging

from dishka import Provider, Scope, provide
import torch

from core import Config
from diarization import DiarizationClient, DiarizationManager, DiarizationService


logger = logging.getLogger(__name__)


class DiarizationProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_diarization_client(self, config: Config) -> AsyncIterator[DiarizationClient]:
        client = DiarizationClient(config.ml.device)
        yield client

        logger.info("Unloading the SpeechBrain model from memory...")
        if hasattr(client, "encoder"):
            del client.encoder
        del client

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()

    @provide(scope=Scope.APP)
    async def get_diarization_service(self, client: DiarizationClient) -> DiarizationService:
        return DiarizationService(client)

    @provide(scope=Scope.APP)
    async def get_manager(self, config: Config, service: DiarizationService) -> DiarizationManager:
        return DiarizationManager(service, config.ml.max_concurrent)
