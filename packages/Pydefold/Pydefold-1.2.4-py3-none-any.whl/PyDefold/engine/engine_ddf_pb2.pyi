from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from gameobject import lua_ddf_pb2 as _lua_ddf_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class HideApp(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class RunScript(_message.Message):
    __slots__ = ["module"]
    MODULE_FIELD_NUMBER: ClassVar[int]
    module: _lua_ddf_pb2.LuaModule
    def __init__(self, module: Optional[Union[_lua_ddf_pb2.LuaModule, Mapping]] = ...) -> None: ...
