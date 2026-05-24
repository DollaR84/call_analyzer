from collections.abc import AsyncIterator
import gc
import logging

from dishka import Provider, Scope, provide
import torch

from core import Config
from transcription import TranscriptionManager, TranscriptionService, WhisperClient


logger = logging.getLogger(__name__)


class TranscriptionProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_whisper_client(self, config: Config) -> AsyncIterator[WhisperClient]:
        client = WhisperClient(config.whisper.model, config.ml.device, config.whisper.compute_type)
        yield client

        logger.info("Unloading the Whisper model from memory...")
        del client

        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        gc.collect()

    @provide(scope=Scope.APP)
    async def get_transcription_service(self, client: WhisperClient) -> TranscriptionService:
        return TranscriptionService(client)

    @provide(scope=Scope.APP)
    async def get_manager(self, config: Config, service: TranscriptionService) -> TranscriptionManager:
        return TranscriptionManager(service, config.ml.max_concurrent)
