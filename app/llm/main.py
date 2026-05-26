import json
import logging
from pathlib import Path
from typing import Any, cast, Optional

from openai import AsyncOpenAI, APIConnectionError, APIStatusError, APITimeoutError, OpenAIError, RateLimitError

from schemas import OutputFiles, Report

from .adapters import BaseModel
from .loader import PromptLoader


logger = logging.getLogger(__name__)


class LLMService:

    def __init__(self, model: BaseModel, prompter: PromptLoader):
        self.model = model
        self.prompter = prompter

        self.client = AsyncOpenAI(
            base_url=self.model.base_url,
            api_key=self.model.api_key,
        )

    def load_context(self, json_file: Path) -> str:
        try:
            return json_file.read_text(encoding="utf-8")

        except OSError as e:
            logger.error("I/O error on file %s: %s", json_file, e)
            raise

    def _clean_llm_json(self, raw_string: str) -> str:
        cleaned = raw_string.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[7:]
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3]

        return cleaned.strip()

    async def process(self, files: OutputFiles) -> Optional[Report]:
        reply: Optional[str] = None
        context = self.load_context(files.json)

        messages: list[dict[str, Any]] = [
            {"role": "system", "content": self.prompter.system},
            {"role": "user", "content": f"[Role: context]\n{context}"},
            {"role": "user", "content": f"[Role: detail]\n{self.prompter.detail}"},
        ]

        try:
            model_name = self.model.get_model_id()
            logger.info("📡 [LLM] query to Model '%s'...", model_name)
            response = await self.client.chat.completions.create(
                model=model_name,
                messages=cast(Any, messages),
                **self.model.params,
            )

            reply = response.choices[0].message.content
            if not reply:
                logger.warning("⚠️ [LLM] Model returned empty content!")
                return None

            report = json.loads(self._clean_llm_json(reply))
            report["file_name"] = files.json.stem
            return Report.model_validate(report)

        except RateLimitError:
            logger.error("🛑 [LLM] Rate limit exceeded! Check billing or limits.")
        except (APIConnectionError, APITimeoutError):
            logger.error("🌐 [LLM] Network issues or OpenAI timeout.")
        except APIStatusError as e:
            logger.error("🏢 [LLM] OpenAI server error: %s", e.status_code)
        except OpenAIError as e:
            logger.error("🧠 [LLM] OpenAI Specific Error: %s", str(e))
        except (json.JSONDecodeError, TypeError) as e:
            logger.error("🧩 [LLM] Failed to parse response as JSON. Error: %s. Raw reply: %s", e, reply)
        except Exception:  # pylint: disable=broad-exception-caught
            logger.exception("🔥 [LLM] Unexpected System Error")

        return None
