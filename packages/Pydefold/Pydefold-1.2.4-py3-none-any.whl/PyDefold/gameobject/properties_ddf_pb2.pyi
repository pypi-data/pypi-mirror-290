from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class PropertyDeclarationEntry(_message.Message):
    __slots__ = ["element_ids", "id", "index", "key"]
    ELEMENT_IDS_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INDEX_FIELD_NUMBER: ClassVar[int]
    KEY_FIELD_NUMBER: ClassVar[int]
    element_ids: _containers.RepeatedScalarFieldContainer[int]
    id: int
    index: int
    key: str
    def __init__(self, key: Optional[str] = ..., id: Optional[int] = ..., index: Optional[int] = ..., element_ids: Optional[Iterable[int]] = ...) -> None: ...

class PropertyDeclarations(_message.Message):
    __slots__ = ["bool_entries", "float_values", "hash_entries", "hash_values", "number_entries", "quat_entries", "string_values", "url_entries", "vector3_entries", "vector4_entries"]
    BOOL_ENTRIES_FIELD_NUMBER: ClassVar[int]
    FLOAT_VALUES_FIELD_NUMBER: ClassVar[int]
    HASH_ENTRIES_FIELD_NUMBER: ClassVar[int]
    HASH_VALUES_FIELD_NUMBER: ClassVar[int]
    NUMBER_ENTRIES_FIELD_NUMBER: ClassVar[int]
    QUAT_ENTRIES_FIELD_NUMBER: ClassVar[int]
    STRING_VALUES_FIELD_NUMBER: ClassVar[int]
    URL_ENTRIES_FIELD_NUMBER: ClassVar[int]
    VECTOR3_ENTRIES_FIELD_NUMBER: ClassVar[int]
    VECTOR4_ENTRIES_FIELD_NUMBER: ClassVar[int]
    bool_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    float_values: _containers.RepeatedScalarFieldContainer[float]
    hash_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    hash_values: _containers.RepeatedScalarFieldContainer[int]
    number_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    quat_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    string_values: _containers.RepeatedScalarFieldContainer[str]
    url_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    vector3_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    vector4_entries: _containers.RepeatedCompositeFieldContainer[PropertyDeclarationEntry]
    def __init__(self, number_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., hash_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., url_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., vector3_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., vector4_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., quat_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., bool_entries: Optional[Iterable[Union[PropertyDeclarationEntry, Mapping]]] = ..., float_values: Optional[Iterable[float]] = ..., hash_values: Optional[Iterable[int]] = ..., string_values: Optional[Iterable[str]] = ...) -> None: ...
