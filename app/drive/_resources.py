from typing import Any, Protocol


class FilesResource(Protocol):

    def list(self, **kwargs: Any) -> Any:
        ...

    def get(self, **kwargs: Any) -> Any:
        ...

    def get_media(self, **kwargs: Any) -> Any:
        ...


class DriveFiles:

    def __init__(self, resource: Any):
        self._resource = resource

    def list(self, **kwargs: Any) -> Any:
        return self._resource.list(**kwargs)

    def get(self, **kwargs: Any) -> Any:
        return self._resource.get(**kwargs)

    def get_media(self, **kwargs: Any) -> Any:
        return self._resource.get_media(**kwargs)
