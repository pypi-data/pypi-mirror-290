from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Reload(_message.Message):
    __slots__ = ["resources"]
    RESOURCES_FIELD_NUMBER: ClassVar[int]
    resources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, resources: Optional[Iterable[str]] = ...) -> None: ...
