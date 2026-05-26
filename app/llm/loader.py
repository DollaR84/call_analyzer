import logging
from pathlib import Path


logger = logging.getLogger(__name__)


class PromptLoader:

    def __init__(self, system_file: Path, detail_file: Path):
        self.system = self.load(system_file)
        self.detail = self.load(detail_file)

    def load(self, prompt_file: Path) -> str:
        try:
            return prompt_file.read_text(encoding="utf-8")
        except FileNotFoundError:
            logger.error("File not found at path: %s", prompt_file)
            raise
        except PermissionError:
            logger.error("No permission to read the file: %s", prompt_file)
            raise
        except OSError as e:
            logger.error("System error when reading a file %s: %s", prompt_file, e)
            raise
