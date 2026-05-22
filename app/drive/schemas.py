from pydantic import BaseModel, Field


class DriveFile(BaseModel):
    id: str
    name: str
    mime_type: str = Field(alias="mimeType")
