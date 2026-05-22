from dishka import AsyncContainer, make_async_container

from .providers import AppProvider, DriveProvider, TranscriberProvider


def get_container() -> AsyncContainer:
    return make_async_container(
        AppProvider(),
        DriveProvider(),
        TranscriberProvider(),
    )
