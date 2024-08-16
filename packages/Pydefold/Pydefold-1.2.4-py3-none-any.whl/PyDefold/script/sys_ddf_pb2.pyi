from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Exit(_message.Message):
    __slots__ = ["code"]
    CODE_FIELD_NUMBER: ClassVar[int]
    code: int
    def __init__(self, code: Optional[int] = ...) -> None: ...

class Reboot(_message.Message):
    __slots__ = ["arg1", "arg2", "arg3", "arg4", "arg5", "arg6"]
    ARG1_FIELD_NUMBER: ClassVar[int]
    ARG2_FIELD_NUMBER: ClassVar[int]
    ARG3_FIELD_NUMBER: ClassVar[int]
    ARG4_FIELD_NUMBER: ClassVar[int]
    ARG5_FIELD_NUMBER: ClassVar[int]
    ARG6_FIELD_NUMBER: ClassVar[int]
    arg1: str
    arg2: str
    arg3: str
    arg4: str
    arg5: str
    arg6: str
    def __init__(self, arg1: Optional[str] = ..., arg2: Optional[str] = ..., arg3: Optional[str] = ..., arg4: Optional[str] = ..., arg5: Optional[str] = ..., arg6: Optional[str] = ...) -> None: ...

class SetUpdateFrequency(_message.Message):
    __slots__ = ["frequency"]
    FREQUENCY_FIELD_NUMBER: ClassVar[int]
    frequency: int
    def __init__(self, frequency: Optional[int] = ...) -> None: ...

class SetVsync(_message.Message):
    __slots__ = ["swap_interval"]
    SWAP_INTERVAL_FIELD_NUMBER: ClassVar[int]
    swap_interval: int
    def __init__(self, swap_interval: Optional[int] = ...) -> None: ...

class StartRecord(_message.Message):
    __slots__ = ["file_name", "fps", "frame_period"]
    FILE_NAME_FIELD_NUMBER: ClassVar[int]
    FPS_FIELD_NUMBER: ClassVar[int]
    FRAME_PERIOD_FIELD_NUMBER: ClassVar[int]
    file_name: str
    fps: int
    frame_period: int
    def __init__(self, file_name: Optional[str] = ..., frame_period: Optional[int] = ..., fps: Optional[int] = ...) -> None: ...

class StopRecord(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class TogglePhysicsDebug(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ToggleProfile(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...
