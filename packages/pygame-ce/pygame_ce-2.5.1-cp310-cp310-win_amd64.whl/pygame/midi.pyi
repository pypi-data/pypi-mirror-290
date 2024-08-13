from typing import List, Tuple, Union

from pygame.event import Event
from ._common import Sequence

MIDIIN: int
MIDIOUT: int

class MidiException(Exception):
    def __init__(self, value: str) -> None: ...

def init() -> None: ...
def quit() -> None: ...
def get_init() -> bool: ...
def get_count() -> int: ...
def get_default_input_id() -> int: ...
def get_default_output_id() -> int: ...
def get_device_info(an_id: int) -> Tuple[str, str, int, int, int]: ...
def midis2events(
    midis: Sequence[Sequence[Union[Sequence[int], int]]], device_id: int
) -> List[Event]: ...
def time() -> int: ...
def frequency_to_midi(frequency: float) -> int: ...
def midi_to_frequency(midi_note: int) -> float: ...
def midi_to_ansi_note(midi_note: int) -> str: ...

class Input:
    device_id: int
    def __init__(self, device_id: int, buffer_size: int = 4096) -> None: ...
    def close(self) -> None: ...
    def poll(self) -> bool: ...
    def read(self, num_events: int) -> List[List[Union[List[int], int]]]: ...

class Output:
    device_id: int
    def __init__(
        self,
        device_id: int,
        latency: int = 0,
        buffer_size: int = 256,
    ) -> None: ...
    def abort(self) -> None: ...
    def close(self) -> None: ...
    def note_off(self, note: int, velocity: int = 0, channel: int = 0) -> None: ...
    def note_on(self, note: int, velocity: int, channel: int = 0) -> None: ...
    def set_instrument(self, instrument_id: int, channel: int = 0) -> None: ...
    def pitch_bend(self, value: int = 0, channel: int = 0) -> None: ...
    def write(self, data: List[List[Union[List[int], int]]]) -> None: ...
    def write_short(self, status: int, data1: int = 0, data2: int = 0) -> None: ...
    def write_sys_ex(self, when: int, msg: Union[List[int], str]) -> None: ...
