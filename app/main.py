import asyncio

from core.container import get_container
from manager import ProcessingManager
from transcription.transcriber import Transcriber


async def main() -> None:
    async with get_container() as container:
        manager = await container.get(ProcessingManager)
        transcriber = await container.get(Transcriber)

        unprocessed = await manager.run_sync()
        await transcriber.process(unprocessed)


if __name__ == "__main__":
    asyncio.run(main())
