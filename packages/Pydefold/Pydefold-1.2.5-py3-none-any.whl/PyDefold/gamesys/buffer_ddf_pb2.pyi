from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
VALUE_TYPE_FLOAT32: ValueType
VALUE_TYPE_INT16: ValueType
VALUE_TYPE_INT32: ValueType
VALUE_TYPE_INT64: ValueType
VALUE_TYPE_INT8: ValueType
VALUE_TYPE_UINT16: ValueType
VALUE_TYPE_UINT32: ValueType
VALUE_TYPE_UINT64: ValueType
VALUE_TYPE_UINT8: ValueType

class BufferDesc(_message.Message):
    __slots__ = ["streams"]
    STREAMS_FIELD_NUMBER: ClassVar[int]
    streams: _containers.RepeatedCompositeFieldContainer[StreamDesc]
    def __init__(self, streams: Optional[Iterable[Union[StreamDesc, Mapping]]] = ...) -> None: ...

class StreamDesc(_message.Message):
    __slots__ = ["f", "i", "i64", "name", "name_hash", "ui", "ui64", "value_count", "value_type"]
    F_FIELD_NUMBER: ClassVar[int]
    I64_FIELD_NUMBER: ClassVar[int]
    I_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    UI64_FIELD_NUMBER: ClassVar[int]
    UI_FIELD_NUMBER: ClassVar[int]
    VALUE_COUNT_FIELD_NUMBER: ClassVar[int]
    VALUE_TYPE_FIELD_NUMBER: ClassVar[int]
    f: _containers.RepeatedScalarFieldContainer[float]
    i: _containers.RepeatedScalarFieldContainer[int]
    i64: _containers.RepeatedScalarFieldContainer[int]
    name: str
    name_hash: int
    ui: _containers.RepeatedScalarFieldContainer[int]
    ui64: _containers.RepeatedScalarFieldContainer[int]
    value_count: int
    value_type: ValueType
    def __init__(self, name: Optional[str] = ..., value_type: Optional[Union[ValueType, str]] = ..., value_count: Optional[int] = ..., ui: Optional[Iterable[int]] = ..., i: Optional[Iterable[int]] = ..., ui64: Optional[Iterable[int]] = ..., i64: Optional[Iterable[int]] = ..., f: Optional[Iterable[float]] = ..., name_hash: Optional[int] = ...) -> None: ...

class ValueType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
