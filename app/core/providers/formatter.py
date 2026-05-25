from dishka import Provider, Scope, provide

from core import Config
from formatters import FormatterManager
from formatters.writers import ExcelWriter, JsonWriter, TxtWriter


class FormatterProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_excel_writer(self, config: Config) -> ExcelWriter:
        return ExcelWriter(config.paths.data_dir)

    @provide(scope=Scope.APP)
    async def get_txt_writer(self, config: Config) -> TxtWriter:
        return TxtWriter(config.paths.transcription_path)

    @provide(scope=Scope.APP)
    async def get_json_writer(self, config: Config) -> JsonWriter:
        return JsonWriter(config.paths.transcription_path)

    @provide(scope=Scope.APP)
    async def get_manager(
            self,
            config: Config,
            excel_writer: ExcelWriter,
            json_writer: JsonWriter,
            txt_writer: TxtWriter,
    ) -> FormatterManager:
        writers = [excel_writer, json_writer, txt_writer]
        return FormatterManager(writers, config.paths.max_concurrent)
