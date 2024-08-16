from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from graphics import graphics_ddf_pb2 as _graphics_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class MaterialDesc(_message.Message):
    __slots__ = ["attributes", "fragment_constants", "fragment_program", "max_page_count", "name", "samplers", "tags", "textures", "vertex_constants", "vertex_program", "vertex_space"]
    class ConstantType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class FilterModeMag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class FilterModeMin(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class VertexSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class WrapMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Constant(_message.Message):
        __slots__ = ["name", "type", "value"]
        NAME_FIELD_NUMBER: ClassVar[int]
        TYPE_FIELD_NUMBER: ClassVar[int]
        VALUE_FIELD_NUMBER: ClassVar[int]
        name: str
        type: MaterialDesc.ConstantType
        value: _containers.RepeatedCompositeFieldContainer[_ddf_math_pb2.Vector4]
        def __init__(self, name: Optional[str] = ..., type: Optional[Union[MaterialDesc.ConstantType, str]] = ..., value: Optional[Iterable[Union[_ddf_math_pb2.Vector4, Mapping]]] = ...) -> None: ...
    class Sampler(_message.Message):
        __slots__ = ["filter_mag", "filter_min", "max_anisotropy", "name", "name_hash", "name_indirections", "texture", "wrap_u", "wrap_v"]
        FILTER_MAG_FIELD_NUMBER: ClassVar[int]
        FILTER_MIN_FIELD_NUMBER: ClassVar[int]
        MAX_ANISOTROPY_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        NAME_HASH_FIELD_NUMBER: ClassVar[int]
        NAME_INDIRECTIONS_FIELD_NUMBER: ClassVar[int]
        TEXTURE_FIELD_NUMBER: ClassVar[int]
        WRAP_U_FIELD_NUMBER: ClassVar[int]
        WRAP_V_FIELD_NUMBER: ClassVar[int]
        filter_mag: MaterialDesc.FilterModeMag
        filter_min: MaterialDesc.FilterModeMin
        max_anisotropy: float
        name: str
        name_hash: int
        name_indirections: _containers.RepeatedScalarFieldContainer[int]
        texture: str
        wrap_u: MaterialDesc.WrapMode
        wrap_v: MaterialDesc.WrapMode
        def __init__(self, name: Optional[str] = ..., wrap_u: Optional[Union[MaterialDesc.WrapMode, str]] = ..., wrap_v: Optional[Union[MaterialDesc.WrapMode, str]] = ..., filter_min: Optional[Union[MaterialDesc.FilterModeMin, str]] = ..., filter_mag: Optional[Union[MaterialDesc.FilterModeMag, str]] = ..., max_anisotropy: Optional[float] = ..., name_indirections: Optional[Iterable[int]] = ..., texture: Optional[str] = ..., name_hash: Optional[int] = ...) -> None: ...
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    CONSTANT_TYPE_NORMAL: MaterialDesc.ConstantType
    CONSTANT_TYPE_PROJECTION: MaterialDesc.ConstantType
    CONSTANT_TYPE_TEXTURE: MaterialDesc.ConstantType
    CONSTANT_TYPE_USER: MaterialDesc.ConstantType
    CONSTANT_TYPE_USER_MATRIX4: MaterialDesc.ConstantType
    CONSTANT_TYPE_VIEW: MaterialDesc.ConstantType
    CONSTANT_TYPE_VIEWPROJ: MaterialDesc.ConstantType
    CONSTANT_TYPE_WORLD: MaterialDesc.ConstantType
    CONSTANT_TYPE_WORLDVIEW: MaterialDesc.ConstantType
    CONSTANT_TYPE_WORLDVIEWPROJ: MaterialDesc.ConstantType
    FILTER_MODE_MAG_DEFAULT: MaterialDesc.FilterModeMag
    FILTER_MODE_MAG_LINEAR: MaterialDesc.FilterModeMag
    FILTER_MODE_MAG_NEAREST: MaterialDesc.FilterModeMag
    FILTER_MODE_MIN_DEFAULT: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_LINEAR: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_LINEAR_MIPMAP_LINEAR: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_LINEAR_MIPMAP_NEAREST: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_NEAREST: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_NEAREST_MIPMAP_LINEAR: MaterialDesc.FilterModeMin
    FILTER_MODE_MIN_NEAREST_MIPMAP_NEAREST: MaterialDesc.FilterModeMin
    FRAGMENT_CONSTANTS_FIELD_NUMBER: ClassVar[int]
    FRAGMENT_PROGRAM_FIELD_NUMBER: ClassVar[int]
    MAX_PAGE_COUNT_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    SAMPLERS_FIELD_NUMBER: ClassVar[int]
    TAGS_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    VERTEX_CONSTANTS_FIELD_NUMBER: ClassVar[int]
    VERTEX_PROGRAM_FIELD_NUMBER: ClassVar[int]
    VERTEX_SPACE_FIELD_NUMBER: ClassVar[int]
    VERTEX_SPACE_LOCAL: MaterialDesc.VertexSpace
    VERTEX_SPACE_WORLD: MaterialDesc.VertexSpace
    WRAP_MODE_CLAMP_TO_EDGE: MaterialDesc.WrapMode
    WRAP_MODE_MIRRORED_REPEAT: MaterialDesc.WrapMode
    WRAP_MODE_REPEAT: MaterialDesc.WrapMode
    attributes: _containers.RepeatedCompositeFieldContainer[_graphics_ddf_pb2.VertexAttribute]
    fragment_constants: _containers.RepeatedCompositeFieldContainer[MaterialDesc.Constant]
    fragment_program: str
    max_page_count: int
    name: str
    samplers: _containers.RepeatedCompositeFieldContainer[MaterialDesc.Sampler]
    tags: _containers.RepeatedScalarFieldContainer[str]
    textures: _containers.RepeatedScalarFieldContainer[str]
    vertex_constants: _containers.RepeatedCompositeFieldContainer[MaterialDesc.Constant]
    vertex_program: str
    vertex_space: MaterialDesc.VertexSpace
    def __init__(self, name: Optional[str] = ..., tags: Optional[Iterable[str]] = ..., vertex_program: Optional[str] = ..., fragment_program: Optional[str] = ..., vertex_space: Optional[Union[MaterialDesc.VertexSpace, str]] = ..., vertex_constants: Optional[Iterable[Union[MaterialDesc.Constant, Mapping]]] = ..., fragment_constants: Optional[Iterable[Union[MaterialDesc.Constant, Mapping]]] = ..., textures: Optional[Iterable[str]] = ..., samplers: Optional[Iterable[Union[MaterialDesc.Sampler, Mapping]]] = ..., max_page_count: Optional[int] = ..., attributes: Optional[Iterable[Union[_graphics_ddf_pb2.VertexAttribute, Mapping]]] = ...) -> None: ...
