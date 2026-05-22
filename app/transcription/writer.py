from pathlib import Path

from .schemas import TranscriptResult


class TranscriptWriter:

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def save(self, result: TranscriptResult) -> Path:
        output_file = self.output_dir / f"{result.file_name}.txt"
        output_file.write_text(result.full_text, encoding="utf-8")
        return output_file
