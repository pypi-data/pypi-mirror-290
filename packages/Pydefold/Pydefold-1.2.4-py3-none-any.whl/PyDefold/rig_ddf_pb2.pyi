from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
INDEXBUFFER_FORMAT_16: IndexBufferFormat
INDEXBUFFER_FORMAT_32: IndexBufferFormat

class AnimationInstanceDesc(_message.Message):
    __slots__ = ["animation"]
    ANIMATION_FIELD_NUMBER: ClassVar[int]
    animation: str
    def __init__(self, animation: Optional[str] = ...) -> None: ...

class AnimationSet(_message.Message):
    __slots__ = ["animations"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    animations: _containers.RepeatedCompositeFieldContainer[RigAnimation]
    def __init__(self, animations: Optional[Iterable[Union[RigAnimation, Mapping]]] = ...) -> None: ...

class AnimationSetDesc(_message.Message):
    __slots__ = ["animations", "skeleton"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    SKELETON_FIELD_NUMBER: ClassVar[int]
    animations: _containers.RepeatedCompositeFieldContainer[AnimationInstanceDesc]
    skeleton: str
    def __init__(self, animations: Optional[Iterable[Union[AnimationInstanceDesc, Mapping]]] = ..., skeleton: Optional[str] = ...) -> None: ...

class AnimationTrack(_message.Message):
    __slots__ = ["bone_id", "positions", "rotations", "scale"]
    BONE_ID_FIELD_NUMBER: ClassVar[int]
    POSITIONS_FIELD_NUMBER: ClassVar[int]
    ROTATIONS_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    bone_id: int
    positions: _containers.RepeatedScalarFieldContainer[float]
    rotations: _containers.RepeatedScalarFieldContainer[float]
    scale: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, bone_id: Optional[int] = ..., positions: Optional[Iterable[float]] = ..., rotations: Optional[Iterable[float]] = ..., scale: Optional[Iterable[float]] = ...) -> None: ...

class Bone(_message.Message):
    __slots__ = ["id", "inverse_bind_pose", "length", "local", "name", "parent", "world"]
    ID_FIELD_NUMBER: ClassVar[int]
    INVERSE_BIND_POSE_FIELD_NUMBER: ClassVar[int]
    LENGTH_FIELD_NUMBER: ClassVar[int]
    LOCAL_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PARENT_FIELD_NUMBER: ClassVar[int]
    WORLD_FIELD_NUMBER: ClassVar[int]
    id: int
    inverse_bind_pose: _ddf_math_pb2.Transform
    length: float
    local: _ddf_math_pb2.Transform
    name: str
    parent: int
    world: _ddf_math_pb2.Transform
    def __init__(self, parent: Optional[int] = ..., id: Optional[int] = ..., name: Optional[str] = ..., local: Optional[Union[_ddf_math_pb2.Transform, Mapping]] = ..., world: Optional[Union[_ddf_math_pb2.Transform, Mapping]] = ..., inverse_bind_pose: Optional[Union[_ddf_math_pb2.Transform, Mapping]] = ..., length: Optional[float] = ...) -> None: ...

class EventKey(_message.Message):
    __slots__ = ["float", "integer", "string", "t"]
    FLOAT_FIELD_NUMBER: ClassVar[int]
    INTEGER_FIELD_NUMBER: ClassVar[int]
    STRING_FIELD_NUMBER: ClassVar[int]
    T_FIELD_NUMBER: ClassVar[int]
    float: float
    integer: int
    string: int
    t: float
    def __init__(self, t: Optional[float] = ..., integer: Optional[int] = ..., float: Optional[float] = ..., string: Optional[int] = ...) -> None: ...

class EventTrack(_message.Message):
    __slots__ = ["event_id", "keys"]
    EVENT_ID_FIELD_NUMBER: ClassVar[int]
    KEYS_FIELD_NUMBER: ClassVar[int]
    event_id: int
    keys: _containers.RepeatedCompositeFieldContainer[EventKey]
    def __init__(self, event_id: Optional[int] = ..., keys: Optional[Iterable[Union[EventKey, Mapping]]] = ...) -> None: ...

class IK(_message.Message):
    __slots__ = ["child", "id", "mix", "parent", "positive", "target"]
    CHILD_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    MIX_FIELD_NUMBER: ClassVar[int]
    PARENT_FIELD_NUMBER: ClassVar[int]
    POSITIVE_FIELD_NUMBER: ClassVar[int]
    TARGET_FIELD_NUMBER: ClassVar[int]
    child: int
    id: int
    mix: float
    parent: int
    positive: bool
    target: int
    def __init__(self, id: Optional[int] = ..., parent: Optional[int] = ..., child: Optional[int] = ..., target: Optional[int] = ..., positive: bool = ..., mix: Optional[float] = ...) -> None: ...

class Mesh(_message.Message):
    __slots__ = ["aabb_max", "aabb_min", "bone_indices", "colors", "indices", "indices_format", "material_index", "normals", "num_texcoord0_components", "num_texcoord1_components", "positions", "tangents", "texcoord0", "texcoord1", "weights"]
    AABB_MAX_FIELD_NUMBER: ClassVar[int]
    AABB_MIN_FIELD_NUMBER: ClassVar[int]
    BONE_INDICES_FIELD_NUMBER: ClassVar[int]
    COLORS_FIELD_NUMBER: ClassVar[int]
    INDICES_FIELD_NUMBER: ClassVar[int]
    INDICES_FORMAT_FIELD_NUMBER: ClassVar[int]
    MATERIAL_INDEX_FIELD_NUMBER: ClassVar[int]
    NORMALS_FIELD_NUMBER: ClassVar[int]
    NUM_TEXCOORD0_COMPONENTS_FIELD_NUMBER: ClassVar[int]
    NUM_TEXCOORD1_COMPONENTS_FIELD_NUMBER: ClassVar[int]
    POSITIONS_FIELD_NUMBER: ClassVar[int]
    TANGENTS_FIELD_NUMBER: ClassVar[int]
    TEXCOORD0_FIELD_NUMBER: ClassVar[int]
    TEXCOORD1_FIELD_NUMBER: ClassVar[int]
    WEIGHTS_FIELD_NUMBER: ClassVar[int]
    aabb_max: _ddf_math_pb2.Vector3
    aabb_min: _ddf_math_pb2.Vector3
    bone_indices: _containers.RepeatedScalarFieldContainer[int]
    colors: _containers.RepeatedScalarFieldContainer[float]
    indices: bytes
    indices_format: IndexBufferFormat
    material_index: int
    normals: _containers.RepeatedScalarFieldContainer[float]
    num_texcoord0_components: int
    num_texcoord1_components: int
    positions: _containers.RepeatedScalarFieldContainer[float]
    tangents: _containers.RepeatedScalarFieldContainer[float]
    texcoord0: _containers.RepeatedScalarFieldContainer[float]
    texcoord1: _containers.RepeatedScalarFieldContainer[float]
    weights: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, aabb_min: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., aabb_max: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., positions: Optional[Iterable[float]] = ..., normals: Optional[Iterable[float]] = ..., tangents: Optional[Iterable[float]] = ..., colors: Optional[Iterable[float]] = ..., texcoord0: Optional[Iterable[float]] = ..., num_texcoord0_components: Optional[int] = ..., texcoord1: Optional[Iterable[float]] = ..., num_texcoord1_components: Optional[int] = ..., indices: Optional[bytes] = ..., indices_format: Optional[Union[IndexBufferFormat, str]] = ..., weights: Optional[Iterable[float]] = ..., bone_indices: Optional[Iterable[int]] = ..., material_index: Optional[int] = ...) -> None: ...

class MeshSet(_message.Message):
    __slots__ = ["bone_list", "materials", "max_bone_count", "models"]
    BONE_LIST_FIELD_NUMBER: ClassVar[int]
    MATERIALS_FIELD_NUMBER: ClassVar[int]
    MAX_BONE_COUNT_FIELD_NUMBER: ClassVar[int]
    MODELS_FIELD_NUMBER: ClassVar[int]
    bone_list: _containers.RepeatedScalarFieldContainer[int]
    materials: _containers.RepeatedScalarFieldContainer[str]
    max_bone_count: int
    models: _containers.RepeatedCompositeFieldContainer[Model]
    def __init__(self, models: Optional[Iterable[Union[Model, Mapping]]] = ..., materials: Optional[Iterable[str]] = ..., bone_list: Optional[Iterable[int]] = ..., max_bone_count: Optional[int] = ...) -> None: ...

class Model(_message.Message):
    __slots__ = ["bone_id", "id", "local", "meshes"]
    BONE_ID_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    LOCAL_FIELD_NUMBER: ClassVar[int]
    MESHES_FIELD_NUMBER: ClassVar[int]
    bone_id: int
    id: int
    local: _ddf_math_pb2.Transform
    meshes: _containers.RepeatedCompositeFieldContainer[Mesh]
    def __init__(self, local: Optional[Union[_ddf_math_pb2.Transform, Mapping]] = ..., id: Optional[int] = ..., meshes: Optional[Iterable[Union[Mesh, Mapping]]] = ..., bone_id: Optional[int] = ...) -> None: ...

class RigAnimation(_message.Message):
    __slots__ = ["duration", "event_tracks", "id", "sample_rate", "tracks"]
    DURATION_FIELD_NUMBER: ClassVar[int]
    EVENT_TRACKS_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    SAMPLE_RATE_FIELD_NUMBER: ClassVar[int]
    TRACKS_FIELD_NUMBER: ClassVar[int]
    duration: float
    event_tracks: _containers.RepeatedCompositeFieldContainer[EventTrack]
    id: int
    sample_rate: float
    tracks: _containers.RepeatedCompositeFieldContainer[AnimationTrack]
    def __init__(self, id: Optional[int] = ..., duration: Optional[float] = ..., sample_rate: Optional[float] = ..., tracks: Optional[Iterable[Union[AnimationTrack, Mapping]]] = ..., event_tracks: Optional[Iterable[Union[EventTrack, Mapping]]] = ...) -> None: ...

class RigScene(_message.Message):
    __slots__ = ["animation_set", "mesh_set", "skeleton", "texture_set"]
    ANIMATION_SET_FIELD_NUMBER: ClassVar[int]
    MESH_SET_FIELD_NUMBER: ClassVar[int]
    SKELETON_FIELD_NUMBER: ClassVar[int]
    TEXTURE_SET_FIELD_NUMBER: ClassVar[int]
    animation_set: str
    mesh_set: str
    skeleton: str
    texture_set: str
    def __init__(self, skeleton: Optional[str] = ..., animation_set: Optional[str] = ..., mesh_set: Optional[str] = ..., texture_set: Optional[str] = ...) -> None: ...

class Skeleton(_message.Message):
    __slots__ = ["bones", "iks"]
    BONES_FIELD_NUMBER: ClassVar[int]
    IKS_FIELD_NUMBER: ClassVar[int]
    bones: _containers.RepeatedCompositeFieldContainer[Bone]
    iks: _containers.RepeatedCompositeFieldContainer[IK]
    def __init__(self, bones: Optional[Iterable[Union[Bone, Mapping]]] = ..., iks: Optional[Iterable[Union[IK, Mapping]]] = ...) -> None: ...

class IndexBufferFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
