from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SoundDesc(_message.Message):
    __slots__ = ["gain", "group", "loopcount", "looping", "pan", "sound", "speed"]
    GAIN_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    LOOPCOUNT_FIELD_NUMBER: ClassVar[int]
    LOOPING_FIELD_NUMBER: ClassVar[int]
    PAN_FIELD_NUMBER: ClassVar[int]
    SOUND_FIELD_NUMBER: ClassVar[int]
    SPEED_FIELD_NUMBER: ClassVar[int]
    gain: float
    group: str
    loopcount: int
    looping: int
    pan: float
    sound: str
    speed: float
    def __init__(self, sound: Optional[str] = ..., looping: Optional[int] = ..., group: Optional[str] = ..., gain: Optional[float] = ..., pan: Optional[float] = ..., speed: Optional[float] = ..., loopcount: Optional[int] = ...) -> None: ...
