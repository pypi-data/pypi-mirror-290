from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from script import lua_source_ddf_pb2 as _lua_source_ddf_pb2
from gameobject import properties_ddf_pb2 as _properties_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LuaModule(_message.Message):
    __slots__ = ["modules", "properties", "property_resources", "resources", "source"]
    MODULES_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    PROPERTY_RESOURCES_FIELD_NUMBER: ClassVar[int]
    RESOURCES_FIELD_NUMBER: ClassVar[int]
    SOURCE_FIELD_NUMBER: ClassVar[int]
    modules: _containers.RepeatedScalarFieldContainer[str]
    properties: _properties_ddf_pb2.PropertyDeclarations
    property_resources: _containers.RepeatedScalarFieldContainer[str]
    resources: _containers.RepeatedScalarFieldContainer[str]
    source: _lua_source_ddf_pb2.LuaSource
    def __init__(self, source: Optional[Union[_lua_source_ddf_pb2.LuaSource, Mapping]] = ..., modules: Optional[Iterable[str]] = ..., resources: Optional[Iterable[str]] = ..., properties: Optional[Union[_properties_ddf_pb2.PropertyDeclarations, Mapping]] = ..., property_resources: Optional[Iterable[str]] = ...) -> None: ...
