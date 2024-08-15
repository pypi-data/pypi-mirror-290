from .typing import Literal, TypedDict


class ResourceVersion(TypedDict):
    semantic_version: str
    state: Literal['published', 'unpublished']
    uuid: str
