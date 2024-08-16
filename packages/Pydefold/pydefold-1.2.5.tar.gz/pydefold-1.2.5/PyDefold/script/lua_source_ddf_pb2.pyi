from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LuaSource(_message.Message):
    __slots__ = ["bytecode", "bytecode_32", "bytecode_64", "delta", "filename", "script"]
    BYTECODE_32_FIELD_NUMBER: ClassVar[int]
    BYTECODE_64_FIELD_NUMBER: ClassVar[int]
    BYTECODE_FIELD_NUMBER: ClassVar[int]
    DELTA_FIELD_NUMBER: ClassVar[int]
    FILENAME_FIELD_NUMBER: ClassVar[int]
    SCRIPT_FIELD_NUMBER: ClassVar[int]
    bytecode: bytes
    bytecode_32: bytes
    bytecode_64: bytes
    delta: bytes
    filename: str
    script: bytes
    def __init__(self, script: Optional[bytes] = ..., filename: Optional[str] = ..., bytecode: Optional[bytes] = ..., delta: Optional[bytes] = ..., bytecode_32: Optional[bytes] = ..., bytecode_64: Optional[bytes] = ...) -> None: ...
