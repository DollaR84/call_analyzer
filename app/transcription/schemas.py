from pydantic import BaseModel


class TranscriptSegment(BaseModel):
    start: float
    end: float
    text: str


class TranscriptResult(BaseModel):
    file_name: str
    full_text: str
    language: str | None = None
    segments: list[TranscriptSegment]
