from typing import TypedDict


class DriveFileResponse(TypedDict):
    id: str
    name: str
    mimeType: str


class DriveListResponse(TypedDict, total=False):
    files: list[DriveFileResponse]
