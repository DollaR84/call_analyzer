import json
import logging
from pathlib import Path

from schemas import Transcript

from .base import BaseWriter


logger = logging.getLogger(__name__)


class JsonWriter(BaseWriter):

    def save(self, data: Transcript) -> Path:
        output_file = self.output_dir / f"{data.file_name}.json"

        json_data = (
            [segment.model_dump(mode="json") for segment in data.segments]
            if data.segments else []
        )

        with output_file.open("w", encoding="utf-8") as file:
            json.dump(json_data, file, ensure_ascii=False, indent=3)

        logger.info("saved json file: %s", output_file.name)
        return output_file
