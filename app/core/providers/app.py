import logging
import warnings

from dishka import Provider, Scope, provide
import torch

from core import Config, get_config
from core.types import Device


warnings.filterwarnings("ignore", module="huggingface_hub")
logging.getLogger("huggingface_hub").setLevel(logging.ERROR)
logger = logging.getLogger(__name__)


class AppProvider(Provider):

    @provide(scope=Scope.APP)
    async def get_config(self) -> Config:
        config = get_config()
        is_available_cuda = torch.cuda.is_available()

        if is_available_cuda and config.ml.device == Device.CPU:
            logger.info("set the device setting 'cuda' to speed things up")

        elif not is_available_cuda and config.ml.device == Device.CUDA:
            logger.info("set the device setting 'cpu' since cuda is not supported")
            config.ml.device = Device.CPU

        return config
