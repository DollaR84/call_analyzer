import logging
from pathlib import Path

from schemas import Transcript


logger = logging.getLogger(__name__)


class TxtWriter:

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def _get_full_text(self, data: Transcript) -> str:
        full_text = data.full_text

        if data.segments and data.segments[0].speaker:
            full_text = "\n".join([
                f"{segment.speaker}: {segment.text}"
                for segment in data.segments
            ])

        return full_text

    def save(self, data: Transcript) -> Path:
        output_file = self.output_dir / f"{data.file_name}.txt"
        full_text = self._get_full_text(data)
        output_file.write_text(full_text, encoding="utf-8")

        logger.info("saved txt file: %s", output_file.name)
        return output_file
