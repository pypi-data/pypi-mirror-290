from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class LuaRef(_message.Message):
    __slots__ = ["context_table_ref", "ref"]
    CONTEXT_TABLE_REF_FIELD_NUMBER: ClassVar[int]
    REF_FIELD_NUMBER: ClassVar[int]
    context_table_ref: int
    ref: int
    def __init__(self, ref: Optional[int] = ..., context_table_ref: Optional[int] = ...) -> None: ...
