import asyncio
from pathlib import Path

from tqdm import tqdm

from .client import WhisperClient
from .schemas import TranscriptResult, TranscriptSegment


class TranscriptionService:

    def __init__(self, client: WhisperClient):
        self.client = client

    def _sync_transcribe(self, audio_path: Path) -> tuple[list[TranscriptSegment], list[str], str]:
        segments, info = self.client.transcribe(str(audio_path))

        result_segments = []
        full_text = []

        with tqdm(total=round(info.duration), unit="sec", desc=f"Transcribing {audio_path.name}") as pbar:
            for seg in segments:
                text = seg.text.strip()

                result_segments.append(
                    TranscriptSegment(
                        start=seg.start,
                        end=seg.end,
                        text=text
                    )
                )
                full_text.append(text)

                pbar.update(round(seg.end) - pbar.n)
            pbar.update(pbar.total - pbar.n)

        return result_segments, full_text, info.language

    async def transcribe(self, audio_path: Path) -> TranscriptResult:
        result_segments, full_text, language = await asyncio.to_thread(
            self._sync_transcribe,
            audio_path
        )

        return TranscriptResult(
            file_name=audio_path.name,
            full_text="\n".join(full_text),
            language=language,
            segments=result_segments
        )
