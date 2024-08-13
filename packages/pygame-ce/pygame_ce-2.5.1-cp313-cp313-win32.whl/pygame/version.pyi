from typing import Literal, Tuple

class SoftwareVersion(Tuple[int, int, int]):
    def __new__(cls, major: int, minor: int, patch: int) -> SoftwareVersion: ...
    def __repr__(self) -> str: ...
    def __str__(self) -> str: ...
    @property
    def major(self) -> int: ...
    @property
    def minor(self) -> int: ...
    @property
    def patch(self) -> int: ...
    fields: Tuple[Literal["major"], Literal["minor"], Literal["patch"]]

class PygameVersion(SoftwareVersion): ...
class SDLVersion(SoftwareVersion): ...

SDL: SDLVersion
ver: str
vernum: PygameVersion
rev: str
