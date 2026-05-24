import logging
import warnings

from dishka import Provider, Scope, provide

from core import Config, get_config


warnings.filterwarnings("ignore", module="huggingface_hub")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        return get_config()
