import asyncio
import logging

from core.container import get_container
from manager import ProcessingManager


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    container = get_container()
    manager = ProcessingManager(container)
    await manager.process()


if __name__ == "__main__":
    asyncio.run(main())
