from dishka import Provider, Scope, provide

from core import Config
from transcription.client import WhisperClient
from transcription.service import TranscriptionService
from transcription.transcriber import Transcriber
from transcription.writer import TranscriptWriter


class TranscriberProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_whisper_client(self, config: Config) -> WhisperClient:
        return WhisperClient(config.whisper)

    @provide(scope=Scope.APP)
    async def get_transcription_service(self, client: WhisperClient) -> TranscriptionService:
        return TranscriptionService(client)

    @provide(scope=Scope.APP)
    async def get_transcriber(
            self,
            config: Config,
            service: TranscriptionService,
            writer: TranscriptWriter,
    ) -> Transcriber:
        return Transcriber(service, writer, config.whisper.max_concurrent)

    @provide(scope=Scope.APP)
    async def get_transcript_writer(self, config: Config) -> TranscriptWriter:
        return TranscriptWriter(config.paths.transcription_path)
