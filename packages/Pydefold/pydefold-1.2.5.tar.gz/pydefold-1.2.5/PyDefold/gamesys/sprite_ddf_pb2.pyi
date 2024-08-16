from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from graphics import graphics_ddf_pb2 as _graphics_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class AnimationDone(_message.Message):
    __slots__ = ["current_tile", "id"]
    CURRENT_TILE_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    current_tile: int
    id: int
    def __init__(self, current_tile: Optional[int] = ..., id: Optional[int] = ...) -> None: ...

class PlayAnimation(_message.Message):
    __slots__ = ["id", "offset", "playback_rate"]
    ID_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: ClassVar[int]
    id: int
    offset: float
    playback_rate: float
    def __init__(self, id: Optional[int] = ..., offset: Optional[float] = ..., playback_rate: Optional[float] = ...) -> None: ...

class SetFlipHorizontal(_message.Message):
    __slots__ = ["flip"]
    FLIP_FIELD_NUMBER: ClassVar[int]
    flip: int
    def __init__(self, flip: Optional[int] = ...) -> None: ...

class SetFlipVertical(_message.Message):
    __slots__ = ["flip"]
    FLIP_FIELD_NUMBER: ClassVar[int]
    flip: int
    def __init__(self, flip: Optional[int] = ...) -> None: ...

class SpriteDesc(_message.Message):
    __slots__ = ["attributes", "blend_mode", "default_animation", "material", "offset", "playback_rate", "size", "size_mode", "slice9", "textures", "tile_set"]
    class BlendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SizeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_ADD: SpriteDesc.BlendMode
    BLEND_MODE_ADD_ALPHA: SpriteDesc.BlendMode
    BLEND_MODE_ALPHA: SpriteDesc.BlendMode
    BLEND_MODE_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_MULT: SpriteDesc.BlendMode
    BLEND_MODE_SCREEN: SpriteDesc.BlendMode
    DEFAULT_ANIMATION_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    SIZE_MODE_AUTO: SpriteDesc.SizeMode
    SIZE_MODE_FIELD_NUMBER: ClassVar[int]
    SIZE_MODE_MANUAL: SpriteDesc.SizeMode
    SLICE9_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    TILE_SET_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_graphics_ddf_pb2.VertexAttribute]
    blend_mode: SpriteDesc.BlendMode
    default_animation: str
    material: str
    offset: float
    playback_rate: float
    size: _ddf_math_pb2.Vector4
    size_mode: SpriteDesc.SizeMode
    slice9: _ddf_math_pb2.Vector4
    textures: _containers.RepeatedCompositeFieldContainer[SpriteTexture]
    tile_set: str
    def __init__(self, tile_set: Optional[str] = ..., default_animation: Optional[str] = ..., material: Optional[str] = ..., blend_mode: Optional[Union[SpriteDesc.BlendMode, str]] = ..., slice9: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., size: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., size_mode: Optional[Union[SpriteDesc.SizeMode, str]] = ..., offset: Optional[float] = ..., playback_rate: Optional[float] = ..., attributes: Optional[Iterable[Union[_graphics_ddf_pb2.VertexAttribute, Mapping]]] = ..., textures: Optional[Iterable[Union[SpriteTexture, Mapping]]] = ...) -> None: ...

class SpriteTexture(_message.Message):
    __slots__ = ["sampler", "texture"]
    SAMPLER_FIELD_NUMBER: ClassVar[int]
    TEXTURE_FIELD_NUMBER: ClassVar[int]
    sampler: str
    texture: str
    def __init__(self, sampler: Optional[str] = ..., texture: Optional[str] = ...) -> None: ...
