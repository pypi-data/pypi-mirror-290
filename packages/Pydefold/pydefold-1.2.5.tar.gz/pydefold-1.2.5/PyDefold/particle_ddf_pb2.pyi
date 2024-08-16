from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from graphics import graphics_ddf_pb2 as _graphics_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

BLEND_MODE_ADD: BlendMode
BLEND_MODE_ADD_ALPHA: BlendMode
BLEND_MODE_ALPHA: BlendMode
BLEND_MODE_MULT: BlendMode
BLEND_MODE_SCREEN: BlendMode
DESCRIPTOR: _descriptor.FileDescriptor
EMISSION_SPACE_EMITTER: EmissionSpace
EMISSION_SPACE_WORLD: EmissionSpace
EMITTER_KEY_COUNT: EmitterKey
EMITTER_KEY_PARTICLE_ALPHA: EmitterKey
EMITTER_KEY_PARTICLE_ANGULAR_VELOCITY: EmitterKey
EMITTER_KEY_PARTICLE_BLUE: EmitterKey
EMITTER_KEY_PARTICLE_GREEN: EmitterKey
EMITTER_KEY_PARTICLE_LIFE_TIME: EmitterKey
EMITTER_KEY_PARTICLE_RED: EmitterKey
EMITTER_KEY_PARTICLE_ROTATION: EmitterKey
EMITTER_KEY_PARTICLE_SIZE: EmitterKey
EMITTER_KEY_PARTICLE_SPEED: EmitterKey
EMITTER_KEY_PARTICLE_STRETCH_FACTOR_X: EmitterKey
EMITTER_KEY_PARTICLE_STRETCH_FACTOR_Y: EmitterKey
EMITTER_KEY_SIZE_X: EmitterKey
EMITTER_KEY_SIZE_Y: EmitterKey
EMITTER_KEY_SIZE_Z: EmitterKey
EMITTER_KEY_SPAWN_RATE: EmitterKey
EMITTER_TYPE_2DCONE: EmitterType
EMITTER_TYPE_BOX: EmitterType
EMITTER_TYPE_CIRCLE: EmitterType
EMITTER_TYPE_CONE: EmitterType
EMITTER_TYPE_SPHERE: EmitterType
MODIFIER_KEY_COUNT: ModifierKey
MODIFIER_KEY_MAGNITUDE: ModifierKey
MODIFIER_KEY_MAX_DISTANCE: ModifierKey
MODIFIER_TYPE_ACCELERATION: ModifierType
MODIFIER_TYPE_DRAG: ModifierType
MODIFIER_TYPE_RADIAL: ModifierType
MODIFIER_TYPE_VORTEX: ModifierType
PARTICLE_KEY_ALPHA: ParticleKey
PARTICLE_KEY_ANGULAR_VELOCITY: ParticleKey
PARTICLE_KEY_BLUE: ParticleKey
PARTICLE_KEY_COUNT: ParticleKey
PARTICLE_KEY_GREEN: ParticleKey
PARTICLE_KEY_RED: ParticleKey
PARTICLE_KEY_ROTATION: ParticleKey
PARTICLE_KEY_SCALE: ParticleKey
PARTICLE_KEY_STRETCH_FACTOR_X: ParticleKey
PARTICLE_KEY_STRETCH_FACTOR_Y: ParticleKey
PARTICLE_ORIENTATION_ANGULAR_VELOCITY: ParticleOrientation
PARTICLE_ORIENTATION_DEFAULT: ParticleOrientation
PARTICLE_ORIENTATION_INITIAL_DIRECTION: ParticleOrientation
PARTICLE_ORIENTATION_MOVEMENT_DIRECTION: ParticleOrientation
PLAY_MODE_LOOP: PlayMode
PLAY_MODE_ONCE: PlayMode
SIZE_MODE_AUTO: SizeMode
SIZE_MODE_MANUAL: SizeMode

class Emitter(_message.Message):
    __slots__ = ["animation", "attributes", "blend_mode", "duration", "duration_spread", "id", "inherit_velocity", "material", "max_particle_count", "mode", "modifiers", "particle_orientation", "particle_properties", "pivot", "position", "properties", "rotation", "size_mode", "space", "start_delay", "start_delay_spread", "start_offset", "stretch_with_velocity", "tile_source", "type"]
    class ParticleProperty(_message.Message):
        __slots__ = ["key", "points"]
        KEY_FIELD_NUMBER: ClassVar[int]
        POINTS_FIELD_NUMBER: ClassVar[int]
        key: ParticleKey
        points: _containers.RepeatedCompositeFieldContainer[SplinePoint]
        def __init__(self, key: Optional[Union[ParticleKey, str]] = ..., points: Optional[Iterable[Union[SplinePoint, Mapping]]] = ...) -> None: ...
    class Property(_message.Message):
        __slots__ = ["key", "points", "spread"]
        KEY_FIELD_NUMBER: ClassVar[int]
        POINTS_FIELD_NUMBER: ClassVar[int]
        SPREAD_FIELD_NUMBER: ClassVar[int]
        key: EmitterKey
        points: _containers.RepeatedCompositeFieldContainer[SplinePoint]
        spread: float
        def __init__(self, key: Optional[Union[EmitterKey, str]] = ..., points: Optional[Iterable[Union[SplinePoint, Mapping]]] = ..., spread: Optional[float] = ...) -> None: ...
    ANIMATION_FIELD_NUMBER: ClassVar[int]
    ATTRIBUTES_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_FIELD_NUMBER: ClassVar[int]
    DURATION_FIELD_NUMBER: ClassVar[int]
    DURATION_SPREAD_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INHERIT_VELOCITY_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    MAX_PARTICLE_COUNT_FIELD_NUMBER: ClassVar[int]
    MODE_FIELD_NUMBER: ClassVar[int]
    MODIFIERS_FIELD_NUMBER: ClassVar[int]
    PARTICLE_ORIENTATION_FIELD_NUMBER: ClassVar[int]
    PARTICLE_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    PIVOT_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SIZE_MODE_FIELD_NUMBER: ClassVar[int]
    SPACE_FIELD_NUMBER: ClassVar[int]
    START_DELAY_FIELD_NUMBER: ClassVar[int]
    START_DELAY_SPREAD_FIELD_NUMBER: ClassVar[int]
    START_OFFSET_FIELD_NUMBER: ClassVar[int]
    STRETCH_WITH_VELOCITY_FIELD_NUMBER: ClassVar[int]
    TILE_SOURCE_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    animation: str
    attributes: _containers.RepeatedCompositeFieldContainer[_graphics_ddf_pb2.VertexAttribute]
    blend_mode: BlendMode
    duration: float
    duration_spread: float
    id: str
    inherit_velocity: float
    material: str
    max_particle_count: int
    mode: PlayMode
    modifiers: _containers.RepeatedCompositeFieldContainer[Modifier]
    particle_orientation: ParticleOrientation
    particle_properties: _containers.RepeatedCompositeFieldContainer[Emitter.ParticleProperty]
    pivot: _ddf_math_pb2.Point3
    position: _ddf_math_pb2.Point3
    properties: _containers.RepeatedCompositeFieldContainer[Emitter.Property]
    rotation: _ddf_math_pb2.Quat
    size_mode: SizeMode
    space: EmissionSpace
    start_delay: float
    start_delay_spread: float
    start_offset: float
    stretch_with_velocity: bool
    tile_source: str
    type: EmitterType
    def __init__(self, id: Optional[str] = ..., mode: Optional[Union[PlayMode, str]] = ..., duration: Optional[float] = ..., space: Optional[Union[EmissionSpace, str]] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., tile_source: Optional[str] = ..., animation: Optional[str] = ..., material: Optional[str] = ..., blend_mode: Optional[Union[BlendMode, str]] = ..., particle_orientation: Optional[Union[ParticleOrientation, str]] = ..., inherit_velocity: Optional[float] = ..., max_particle_count: Optional[int] = ..., type: Optional[Union[EmitterType, str]] = ..., start_delay: Optional[float] = ..., properties: Optional[Iterable[Union[Emitter.Property, Mapping]]] = ..., particle_properties: Optional[Iterable[Union[Emitter.ParticleProperty, Mapping]]] = ..., modifiers: Optional[Iterable[Union[Modifier, Mapping]]] = ..., size_mode: Optional[Union[SizeMode, str]] = ..., start_delay_spread: Optional[float] = ..., duration_spread: Optional[float] = ..., stretch_with_velocity: bool = ..., start_offset: Optional[float] = ..., pivot: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., attributes: Optional[Iterable[Union[_graphics_ddf_pb2.VertexAttribute, Mapping]]] = ...) -> None: ...

class Modifier(_message.Message):
    __slots__ = ["position", "properties", "rotation", "type", "use_direction"]
    class Property(_message.Message):
        __slots__ = ["key", "points", "spread"]
        KEY_FIELD_NUMBER: ClassVar[int]
        POINTS_FIELD_NUMBER: ClassVar[int]
        SPREAD_FIELD_NUMBER: ClassVar[int]
        key: ModifierKey
        points: _containers.RepeatedCompositeFieldContainer[SplinePoint]
        spread: float
        def __init__(self, key: Optional[Union[ModifierKey, str]] = ..., points: Optional[Iterable[Union[SplinePoint, Mapping]]] = ..., spread: Optional[float] = ...) -> None: ...
    POSITION_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    USE_DIRECTION_FIELD_NUMBER: ClassVar[int]
    position: _ddf_math_pb2.Point3
    properties: _containers.RepeatedCompositeFieldContainer[Modifier.Property]
    rotation: _ddf_math_pb2.Quat
    type: ModifierType
    use_direction: int
    def __init__(self, type: Optional[Union[ModifierType, str]] = ..., use_direction: Optional[int] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., properties: Optional[Iterable[Union[Modifier.Property, Mapping]]] = ...) -> None: ...

class ParticleFX(_message.Message):
    __slots__ = ["emitters", "modifiers"]
    EMITTERS_FIELD_NUMBER: ClassVar[int]
    MODIFIERS_FIELD_NUMBER: ClassVar[int]
    emitters: _containers.RepeatedCompositeFieldContainer[Emitter]
    modifiers: _containers.RepeatedCompositeFieldContainer[Modifier]
    def __init__(self, emitters: Optional[Iterable[Union[Emitter, Mapping]]] = ..., modifiers: Optional[Iterable[Union[Modifier, Mapping]]] = ...) -> None: ...

class SplinePoint(_message.Message):
    __slots__ = ["t_x", "t_y", "x", "y"]
    T_X_FIELD_NUMBER: ClassVar[int]
    T_Y_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    t_x: float
    t_y: float
    x: float
    y: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., t_x: Optional[float] = ..., t_y: Optional[float] = ...) -> None: ...

class EmitterType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class PlayMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class EmissionSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class EmitterKey(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ParticleKey(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ModifierType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ModifierKey(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class BlendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SizeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class ParticleOrientation(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
