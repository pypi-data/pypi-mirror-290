from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from graphics import graphics_ddf_pb2 as _graphics_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Material(_message.Message):
    __slots__ = ["attributes", "material", "name", "textures"]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    attributes: _containers.RepeatedCompositeFieldContainer[_graphics_ddf_pb2.VertexAttribute]
    material: str
    name: str
    textures: _containers.RepeatedCompositeFieldContainer[Texture]
    def __init__(self, name: Optional[str] = ..., material: Optional[str] = ..., textures: Optional[Iterable[Union[Texture, Mapping]]] = ..., attributes: Optional[Iterable[Union[_graphics_ddf_pb2.VertexAttribute, Mapping]]] = ...) -> None: ...

class Model(_message.Message):
    __slots__ = ["default_animation", "materials", "rig_scene"]
    DEFAULT_ANIMATION_FIELD_NUMBER: ClassVar[int]
    MATERIALS_FIELD_NUMBER: ClassVar[int]
    RIG_SCENE_FIELD_NUMBER: ClassVar[int]
    default_animation: str
    materials: _containers.RepeatedCompositeFieldContainer[Material]
    rig_scene: str
    def __init__(self, rig_scene: Optional[str] = ..., default_animation: Optional[str] = ..., materials: Optional[Iterable[Union[Material, Mapping]]] = ...) -> None: ...

class ModelAnimationDone(_message.Message):
    __slots__ = ["animation_id", "playback"]
    ANIMATION_ID_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_FIELD_NUMBER: ClassVar[int]
    animation_id: int
    playback: int
    def __init__(self, animation_id: Optional[int] = ..., playback: Optional[int] = ...) -> None: ...

class ModelCancelAnimation(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ModelDesc(_message.Message):
    __slots__ = ["animations", "default_animation", "material", "materials", "mesh", "name", "skeleton", "textures"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    DEFAULT_ANIMATION_FIELD_NUMBER: ClassVar[int]
    MATERIALS_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    MESH_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    SKELETON_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    animations: str
    default_animation: str
    material: str
    materials: _containers.RepeatedCompositeFieldContainer[Material]
    mesh: str
    name: str
    skeleton: str
    textures: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, mesh: Optional[str] = ..., material: Optional[str] = ..., textures: Optional[Iterable[str]] = ..., skeleton: Optional[str] = ..., animations: Optional[str] = ..., default_animation: Optional[str] = ..., name: Optional[str] = ..., materials: Optional[Iterable[Union[Material, Mapping]]] = ...) -> None: ...

class ModelPlayAnimation(_message.Message):
    __slots__ = ["animation_id", "blend_duration", "offset", "playback", "playback_rate"]
    ANIMATION_ID_FIELD_NUMBER: ClassVar[int]
    BLEND_DURATION_FIELD_NUMBER: ClassVar[int]
    OFFSET_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_RATE_FIELD_NUMBER: ClassVar[int]
    animation_id: int
    blend_duration: float
    offset: float
    playback: int
    playback_rate: float
    def __init__(self, animation_id: Optional[int] = ..., playback: Optional[int] = ..., blend_duration: Optional[float] = ..., offset: Optional[float] = ..., playback_rate: Optional[float] = ...) -> None: ...

class ResetConstant(_message.Message):
    __slots__ = ["name_hash"]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    name_hash: int
    def __init__(self, name_hash: Optional[int] = ...) -> None: ...

class SetTexture(_message.Message):
    __slots__ = ["texture_hash", "texture_unit"]
    TEXTURE_HASH_FIELD_NUMBER: ClassVar[int]
    TEXTURE_UNIT_FIELD_NUMBER: ClassVar[int]
    texture_hash: int
    texture_unit: int
    def __init__(self, texture_hash: Optional[int] = ..., texture_unit: Optional[int] = ...) -> None: ...

class Texture(_message.Message):
    __slots__ = ["sampler", "texture"]
    SAMPLER_FIELD_NUMBER: ClassVar[int]
    TEXTURE_FIELD_NUMBER: ClassVar[int]
    sampler: str
    texture: str
    def __init__(self, sampler: Optional[str] = ..., texture: Optional[str] = ...) -> None: ...
