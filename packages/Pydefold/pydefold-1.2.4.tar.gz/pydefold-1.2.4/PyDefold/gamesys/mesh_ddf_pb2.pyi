from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class MeshDesc(_message.Message):
    __slots__ = ["material", "normal_stream", "position_stream", "primitive_type", "textures", "vertices"]
    class PrimitiveType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    NORMAL_STREAM_FIELD_NUMBER: ClassVar[int]
    POSITION_STREAM_FIELD_NUMBER: ClassVar[int]
    PRIMITIVE_LINES: MeshDesc.PrimitiveType
    PRIMITIVE_TRIANGLES: MeshDesc.PrimitiveType
    PRIMITIVE_TRIANGLE_STRIP: MeshDesc.PrimitiveType
    PRIMITIVE_TYPE_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    VERTICES_FIELD_NUMBER: ClassVar[int]
    material: str
    normal_stream: str
    position_stream: str
    primitive_type: MeshDesc.PrimitiveType
    textures: _containers.RepeatedScalarFieldContainer[str]
    vertices: str
    def __init__(self, material: Optional[str] = ..., vertices: Optional[str] = ..., textures: Optional[Iterable[str]] = ..., primitive_type: Optional[Union[MeshDesc.PrimitiveType, str]] = ..., position_stream: Optional[str] = ..., normal_stream: Optional[str] = ...) -> None: ...
