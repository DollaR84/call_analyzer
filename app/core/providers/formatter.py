from dishka import Provider, Scope, provide

from core import Config
from formatters import FormatterManager, JsonWriter, TxtWriter


class FormatterProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_txt_writer(self, config: Config) -> TxtWriter:
        return TxtWriter(config.paths.transcription_path)

    @provide(scope=Scope.APP)
    async def get_json_writer(self, config: Config) -> JsonWriter:
        return JsonWriter(config.paths.transcription_path)

    @provide(scope=Scope.APP)
    async def get_manager(self, config: Config, json_writer: JsonWriter, txt_writer: TxtWriter) -> FormatterManager:
        return FormatterManager(json_writer, txt_writer, config.paths.max_concurrent)
