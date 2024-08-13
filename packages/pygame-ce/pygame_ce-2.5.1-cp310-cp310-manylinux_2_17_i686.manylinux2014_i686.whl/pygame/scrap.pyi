from typing import List, Optional
from typing_extensions import deprecated # added in 3.13
from collections.abc import ByteString

@deprecated("since 2.2.0. Use the new API instead, which only requires display init")
def init() -> None: ...
@deprecated("since 2.2.0. Use the new API instead, which doesn't require scrap init")
def get_init() -> bool: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.get_text`")
def get(data_type: str, /) -> Optional[bytes]: ...
@deprecated("since 2.2.0. Use the new API instead, which only supports strings")
def get_types() -> List[str]: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.put_text`")
def put(data_type: str, data: ByteString, /) -> None: ...
@deprecated("since 2.2.0. Use the new API instead: `pygame.scrap.has_text`")
def contains(data_type: str, /) -> bool: ...
@deprecated("since 2.2.0. Use the new API instead, which uses system clipboard")
def lost() -> bool: ...
@deprecated("since 2.2.0. Use the new API instead, which only supports strings")
def set_mode(mode: int, /) -> None: ...
def put_text(text: str, /) -> None: ...
def get_text() -> str: ...
def has_text() -> bool: ...
