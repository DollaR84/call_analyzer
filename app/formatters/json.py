import json
import logging
from pathlib import Path

from schemas import Transcript


logger = logging.getLogger(__name__)


class JsonWriter:

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, transcript: Transcript) -> Path:
        output_file = self.output_dir / f"{transcript.file_name}.json"

        data = (
            [segment.model_dump(mode="json") for segment in transcript.segments]
            if transcript.segments else []
        )

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=3)

        logger.info("saved json file: %s", output_file.name)
        return output_file
