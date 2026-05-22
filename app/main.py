import asyncio
import logging

from core.container import get_container
from manager import ProcessingManager
from transcription.transcriber import Transcriber


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)
logger = logging.getLogger(__name__)


async def main() -> None:
    async with get_container() as container:
        manager = await container.get(ProcessingManager)
        transcriber = await container.get(Transcriber)

        unprocessed = await manager.run_sync()
        await transcriber.process(unprocessed)
        logger.info("processed %d files", len(unprocessed))


if __name__ == "__main__":
    asyncio.run(main())
