from dishka import AsyncContainer, make_async_container

from .providers import (
    AppProvider,
    DriveProvider,
    DiarizationProvider,
    TranscriptionProvider,
    FormatterProvider,
    LLMProvider,
)


def get_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        DriveProvider(),
        TranscriptionProvider(),
        DiarizationProvider(),
        FormatterProvider(),
        LLMProvider(),
    )
