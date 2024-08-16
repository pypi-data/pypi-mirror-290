from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
POINT: LightType
SPOT: LightType
TIME_STEP_MODE_CONTINUOUS: TimeStepMode
TIME_STEP_MODE_DISCRETE: TimeStepMode

class CollectionFactoryDesc(_message.Message):
    __slots__ = ["dynamic_prototype", "load_dynamically", "prototype"]
    DYNAMIC_PROTOTYPE_FIELD_NUMBER: ClassVar[int]
    LOAD_DYNAMICALLY_FIELD_NUMBER: ClassVar[int]
    PROTOTYPE_FIELD_NUMBER: ClassVar[int]
    dynamic_prototype: bool
    load_dynamically: bool
    prototype: str
    def __init__(self, prototype: Optional[str] = ..., load_dynamically: bool = ..., dynamic_prototype: bool = ...) -> None: ...

class CollectionProxyDesc(_message.Message):
    __slots__ = ["collection", "exclude"]
    COLLECTION_FIELD_NUMBER: ClassVar[int]
    EXCLUDE_FIELD_NUMBER: ClassVar[int]
    collection: str
    exclude: bool
    def __init__(self, collection: Optional[str] = ..., exclude: bool = ...) -> None: ...

class Create(_message.Message):
    __slots__ = ["id", "index", "position", "rotation", "scale", "scale3"]
    ID_FIELD_NUMBER: ClassVar[int]
    INDEX_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE3_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    id: int
    index: int
    position: _ddf_math_pb2.Point3
    rotation: _ddf_math_pb2.Quat
    scale: float
    scale3: _ddf_math_pb2.Vector3
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., id: Optional[int] = ..., scale: Optional[float] = ..., scale3: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., index: Optional[int] = ...) -> None: ...

class FactoryDesc(_message.Message):
    __slots__ = ["dynamic_prototype", "load_dynamically", "prototype"]
    DYNAMIC_PROTOTYPE_FIELD_NUMBER: ClassVar[int]
    LOAD_DYNAMICALLY_FIELD_NUMBER: ClassVar[int]
    PROTOTYPE_FIELD_NUMBER: ClassVar[int]
    dynamic_prototype: bool
    load_dynamically: bool
    prototype: str
    def __init__(self, prototype: Optional[str] = ..., load_dynamically: bool = ..., dynamic_prototype: bool = ...) -> None: ...

class LightDesc(_message.Message):
    __slots__ = ["color", "cone_angle", "decay", "drop_off", "id", "intensity", "penumbra_angle", "range", "type"]
    COLOR_FIELD_NUMBER: ClassVar[int]
    CONE_ANGLE_FIELD_NUMBER: ClassVar[int]
    DECAY_FIELD_NUMBER: ClassVar[int]
    DROP_OFF_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INTENSITY_FIELD_NUMBER: ClassVar[int]
    PENUMBRA_ANGLE_FIELD_NUMBER: ClassVar[int]
    RANGE_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    color: _ddf_math_pb2.Vector3
    cone_angle: float
    decay: float
    drop_off: float
    id: str
    intensity: float
    penumbra_angle: float
    range: float
    type: LightType
    def __init__(self, id: Optional[str] = ..., type: Optional[Union[LightType, str]] = ..., intensity: Optional[float] = ..., color: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., range: Optional[float] = ..., decay: Optional[float] = ..., cone_angle: Optional[float] = ..., penumbra_angle: Optional[float] = ..., drop_off: Optional[float] = ...) -> None: ...

class PauseSound(_message.Message):
    __slots__ = ["pause"]
    PAUSE_FIELD_NUMBER: ClassVar[int]
    pause: bool
    def __init__(self, pause: bool = ...) -> None: ...

class PlayParticleFX(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class PlaySound(_message.Message):
    __slots__ = ["delay", "gain", "pan", "play_id", "speed"]
    DELAY_FIELD_NUMBER: ClassVar[int]
    GAIN_FIELD_NUMBER: ClassVar[int]
    PAN_FIELD_NUMBER: ClassVar[int]
    PLAY_ID_FIELD_NUMBER: ClassVar[int]
    SPEED_FIELD_NUMBER: ClassVar[int]
    delay: float
    gain: float
    pan: float
    play_id: int
    speed: float
    def __init__(self, delay: Optional[float] = ..., gain: Optional[float] = ..., pan: Optional[float] = ..., speed: Optional[float] = ..., play_id: Optional[int] = ...) -> None: ...

class ResetConstant(_message.Message):
    __slots__ = ["name_hash"]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    name_hash: int
    def __init__(self, name_hash: Optional[int] = ...) -> None: ...

class ResetConstantParticleFX(_message.Message):
    __slots__ = ["emitter_id", "name_hash"]
    EMITTER_ID_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    emitter_id: int
    name_hash: int
    def __init__(self, emitter_id: Optional[int] = ..., name_hash: Optional[int] = ...) -> None: ...

class SetConstant(_message.Message):
    __slots__ = ["index", "name_hash", "value"]
    INDEX_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    index: int
    name_hash: int
    value: _ddf_math_pb2.Vector4
    def __init__(self, name_hash: Optional[int] = ..., value: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., index: Optional[int] = ...) -> None: ...

class SetConstantParticleFX(_message.Message):
    __slots__ = ["emitter_id", "is_matrix4", "name_hash", "value"]
    EMITTER_ID_FIELD_NUMBER: ClassVar[int]
    IS_MATRIX4_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    emitter_id: int
    is_matrix4: bool
    name_hash: int
    value: _ddf_math_pb2.Matrix4
    def __init__(self, emitter_id: Optional[int] = ..., name_hash: Optional[int] = ..., value: Optional[Union[_ddf_math_pb2.Matrix4, Mapping]] = ..., is_matrix4: bool = ...) -> None: ...

class SetGain(_message.Message):
    __slots__ = ["gain"]
    GAIN_FIELD_NUMBER: ClassVar[int]
    gain: float
    def __init__(self, gain: Optional[float] = ...) -> None: ...

class SetLight(_message.Message):
    __slots__ = ["light", "position", "rotation"]
    LIGHT_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    light: LightDesc
    position: _ddf_math_pb2.Point3
    rotation: _ddf_math_pb2.Quat
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., light: Optional[Union[LightDesc, Mapping]] = ...) -> None: ...

class SetPan(_message.Message):
    __slots__ = ["pan"]
    PAN_FIELD_NUMBER: ClassVar[int]
    pan: float
    def __init__(self, pan: Optional[float] = ...) -> None: ...

class SetScale(_message.Message):
    __slots__ = ["scale"]
    SCALE_FIELD_NUMBER: ClassVar[int]
    scale: _ddf_math_pb2.Vector3
    def __init__(self, scale: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ...) -> None: ...

class SetSpeed(_message.Message):
    __slots__ = ["speed"]
    SPEED_FIELD_NUMBER: ClassVar[int]
    speed: float
    def __init__(self, speed: Optional[float] = ...) -> None: ...

class SetTimeStep(_message.Message):
    __slots__ = ["factor", "mode"]
    FACTOR_FIELD_NUMBER: ClassVar[int]
    MODE_FIELD_NUMBER: ClassVar[int]
    factor: float
    mode: TimeStepMode
    def __init__(self, factor: Optional[float] = ..., mode: Optional[Union[TimeStepMode, str]] = ...) -> None: ...

class SetViewProjection(_message.Message):
    __slots__ = ["id", "projection", "view"]
    ID_FIELD_NUMBER: ClassVar[int]
    PROJECTION_FIELD_NUMBER: ClassVar[int]
    VIEW_FIELD_NUMBER: ClassVar[int]
    id: int
    projection: _ddf_math_pb2.Matrix4
    view: _ddf_math_pb2.Matrix4
    def __init__(self, id: Optional[int] = ..., view: Optional[Union[_ddf_math_pb2.Matrix4, Mapping]] = ..., projection: Optional[Union[_ddf_math_pb2.Matrix4, Mapping]] = ...) -> None: ...

class SoundEvent(_message.Message):
    __slots__ = ["play_id"]
    PLAY_ID_FIELD_NUMBER: ClassVar[int]
    play_id: int
    def __init__(self, play_id: Optional[int] = ...) -> None: ...

class StopParticleFX(_message.Message):
    __slots__ = ["clear_particles"]
    CLEAR_PARTICLES_FIELD_NUMBER: ClassVar[int]
    clear_particles: bool
    def __init__(self, clear_particles: bool = ...) -> None: ...

class StopSound(_message.Message):
    __slots__ = ["play_id"]
    PLAY_ID_FIELD_NUMBER: ClassVar[int]
    play_id: int
    def __init__(self, play_id: Optional[int] = ...) -> None: ...

class TimeStepMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class LightType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
