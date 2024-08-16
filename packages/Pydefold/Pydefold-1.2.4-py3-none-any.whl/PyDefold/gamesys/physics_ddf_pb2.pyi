from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

COLLISION_OBJECT_TYPE_DYNAMIC: CollisionObjectType
COLLISION_OBJECT_TYPE_KINEMATIC: CollisionObjectType
COLLISION_OBJECT_TYPE_STATIC: CollisionObjectType
COLLISION_OBJECT_TYPE_TRIGGER: CollisionObjectType
DESCRIPTOR: _descriptor.FileDescriptor

class ApplyForce(_message.Message):
    __slots__ = ["force", "position"]
    FORCE_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    force: _ddf_math_pb2.Vector3
    position: _ddf_math_pb2.Point3
    def __init__(self, force: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ...) -> None: ...

class Collision(_message.Message):
    __slots__ = ["group", "id", "position"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    group: int
    id: int
    position: _ddf_math_pb2.Point3
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., id: Optional[int] = ..., group: Optional[int] = ...) -> None: ...

class CollisionEvent(_message.Message):
    __slots__ = ["a", "b"]
    A_FIELD_NUMBER: ClassVar[int]
    B_FIELD_NUMBER: ClassVar[int]
    a: Collision
    b: Collision
    def __init__(self, a: Optional[Union[Collision, Mapping]] = ..., b: Optional[Union[Collision, Mapping]] = ...) -> None: ...

class CollisionObjectDesc(_message.Message):
    __slots__ = ["angular_damping", "bullet", "collision_shape", "embedded_collision_shape", "friction", "group", "linear_damping", "locked_rotation", "mask", "mass", "restitution", "type"]
    ANGULAR_DAMPING_FIELD_NUMBER: ClassVar[int]
    BULLET_FIELD_NUMBER: ClassVar[int]
    COLLISION_SHAPE_FIELD_NUMBER: ClassVar[int]
    EMBEDDED_COLLISION_SHAPE_FIELD_NUMBER: ClassVar[int]
    FRICTION_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    LINEAR_DAMPING_FIELD_NUMBER: ClassVar[int]
    LOCKED_ROTATION_FIELD_NUMBER: ClassVar[int]
    MASK_FIELD_NUMBER: ClassVar[int]
    MASS_FIELD_NUMBER: ClassVar[int]
    RESTITUTION_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    angular_damping: float
    bullet: bool
    collision_shape: str
    embedded_collision_shape: CollisionShape
    friction: float
    group: str
    linear_damping: float
    locked_rotation: bool
    mask: _containers.RepeatedScalarFieldContainer[str]
    mass: float
    restitution: float
    type: CollisionObjectType
    def __init__(self, collision_shape: Optional[str] = ..., type: Optional[Union[CollisionObjectType, str]] = ..., mass: Optional[float] = ..., friction: Optional[float] = ..., restitution: Optional[float] = ..., group: Optional[str] = ..., mask: Optional[Iterable[str]] = ..., embedded_collision_shape: Optional[Union[CollisionShape, Mapping]] = ..., linear_damping: Optional[float] = ..., angular_damping: Optional[float] = ..., locked_rotation: bool = ..., bullet: bool = ...) -> None: ...

class CollisionResponse(_message.Message):
    __slots__ = ["group", "other_group", "other_id", "other_position", "own_group"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    OTHER_GROUP_FIELD_NUMBER: ClassVar[int]
    OTHER_ID_FIELD_NUMBER: ClassVar[int]
    OTHER_POSITION_FIELD_NUMBER: ClassVar[int]
    OWN_GROUP_FIELD_NUMBER: ClassVar[int]
    group: int
    other_group: int
    other_id: int
    other_position: _ddf_math_pb2.Point3
    own_group: int
    def __init__(self, other_id: Optional[int] = ..., group: Optional[int] = ..., other_position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., other_group: Optional[int] = ..., own_group: Optional[int] = ...) -> None: ...

class CollisionShape(_message.Message):
    __slots__ = ["data", "shapes"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Shape(_message.Message):
        __slots__ = ["count", "id", "id_hash", "index", "position", "rotation", "shape_type"]
        COUNT_FIELD_NUMBER: ClassVar[int]
        ID_FIELD_NUMBER: ClassVar[int]
        ID_HASH_FIELD_NUMBER: ClassVar[int]
        INDEX_FIELD_NUMBER: ClassVar[int]
        POSITION_FIELD_NUMBER: ClassVar[int]
        ROTATION_FIELD_NUMBER: ClassVar[int]
        SHAPE_TYPE_FIELD_NUMBER: ClassVar[int]
        count: int
        id: str
        id_hash: int
        index: int
        position: _ddf_math_pb2.Point3
        rotation: _ddf_math_pb2.Quat
        shape_type: CollisionShape.Type
        def __init__(self, shape_type: Optional[Union[CollisionShape.Type, str]] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., index: Optional[int] = ..., count: Optional[int] = ..., id: Optional[str] = ..., id_hash: Optional[int] = ...) -> None: ...
    DATA_FIELD_NUMBER: ClassVar[int]
    SHAPES_FIELD_NUMBER: ClassVar[int]
    TYPE_BOX: CollisionShape.Type
    TYPE_CAPSULE: CollisionShape.Type
    TYPE_HULL: CollisionShape.Type
    TYPE_SPHERE: CollisionShape.Type
    data: _containers.RepeatedScalarFieldContainer[float]
    shapes: _containers.RepeatedCompositeFieldContainer[CollisionShape.Shape]
    def __init__(self, shapes: Optional[Iterable[Union[CollisionShape.Shape, Mapping]]] = ..., data: Optional[Iterable[float]] = ...) -> None: ...

class ContactPoint(_message.Message):
    __slots__ = ["group", "id", "mass", "normal", "position", "relative_velocity"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    MASS_FIELD_NUMBER: ClassVar[int]
    NORMAL_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: ClassVar[int]
    group: int
    id: int
    mass: float
    normal: _ddf_math_pb2.Vector3
    position: _ddf_math_pb2.Point3
    relative_velocity: _ddf_math_pb2.Vector3
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., normal: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., relative_velocity: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., mass: Optional[float] = ..., id: Optional[int] = ..., group: Optional[int] = ...) -> None: ...

class ContactPointEvent(_message.Message):
    __slots__ = ["a", "applied_impulse", "b", "distance"]
    APPLIED_IMPULSE_FIELD_NUMBER: ClassVar[int]
    A_FIELD_NUMBER: ClassVar[int]
    B_FIELD_NUMBER: ClassVar[int]
    DISTANCE_FIELD_NUMBER: ClassVar[int]
    a: ContactPoint
    applied_impulse: float
    b: ContactPoint
    distance: float
    def __init__(self, a: Optional[Union[ContactPoint, Mapping]] = ..., b: Optional[Union[ContactPoint, Mapping]] = ..., distance: Optional[float] = ..., applied_impulse: Optional[float] = ...) -> None: ...

class ContactPointResponse(_message.Message):
    __slots__ = ["applied_impulse", "distance", "group", "life_time", "mass", "normal", "other_group", "other_id", "other_mass", "other_position", "own_group", "position", "relative_velocity"]
    APPLIED_IMPULSE_FIELD_NUMBER: ClassVar[int]
    DISTANCE_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    LIFE_TIME_FIELD_NUMBER: ClassVar[int]
    MASS_FIELD_NUMBER: ClassVar[int]
    NORMAL_FIELD_NUMBER: ClassVar[int]
    OTHER_GROUP_FIELD_NUMBER: ClassVar[int]
    OTHER_ID_FIELD_NUMBER: ClassVar[int]
    OTHER_MASS_FIELD_NUMBER: ClassVar[int]
    OTHER_POSITION_FIELD_NUMBER: ClassVar[int]
    OWN_GROUP_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    RELATIVE_VELOCITY_FIELD_NUMBER: ClassVar[int]
    applied_impulse: float
    distance: float
    group: int
    life_time: float
    mass: float
    normal: _ddf_math_pb2.Vector3
    other_group: int
    other_id: int
    other_mass: float
    other_position: _ddf_math_pb2.Point3
    own_group: int
    position: _ddf_math_pb2.Point3
    relative_velocity: _ddf_math_pb2.Vector3
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., normal: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., relative_velocity: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., distance: Optional[float] = ..., applied_impulse: Optional[float] = ..., life_time: Optional[float] = ..., mass: Optional[float] = ..., other_mass: Optional[float] = ..., other_id: Optional[int] = ..., other_position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., group: Optional[int] = ..., other_group: Optional[int] = ..., own_group: Optional[int] = ...) -> None: ...

class ConvexShape(_message.Message):
    __slots__ = ["data", "shape_type"]
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    DATA_FIELD_NUMBER: ClassVar[int]
    SHAPE_TYPE_FIELD_NUMBER: ClassVar[int]
    TYPE_BOX: ConvexShape.Type
    TYPE_CAPSULE: ConvexShape.Type
    TYPE_HULL: ConvexShape.Type
    TYPE_SPHERE: ConvexShape.Type
    data: _containers.RepeatedScalarFieldContainer[float]
    shape_type: ConvexShape.Type
    def __init__(self, shape_type: Optional[Union[ConvexShape.Type, str]] = ..., data: Optional[Iterable[float]] = ...) -> None: ...

class EnableGridShapeLayer(_message.Message):
    __slots__ = ["enable", "shape"]
    ENABLE_FIELD_NUMBER: ClassVar[int]
    SHAPE_FIELD_NUMBER: ClassVar[int]
    enable: int
    shape: int
    def __init__(self, shape: Optional[int] = ..., enable: Optional[int] = ...) -> None: ...

class RayCastMissed(_message.Message):
    __slots__ = ["request_id"]
    REQUEST_ID_FIELD_NUMBER: ClassVar[int]
    request_id: int
    def __init__(self, request_id: Optional[int] = ...) -> None: ...

class RayCastResponse(_message.Message):
    __slots__ = ["fraction", "group", "id", "normal", "position", "request_id"]
    FRACTION_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    NORMAL_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: ClassVar[int]
    fraction: float
    group: int
    id: int
    normal: _ddf_math_pb2.Vector3
    position: _ddf_math_pb2.Point3
    request_id: int
    def __init__(self, fraction: Optional[float] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., normal: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., id: Optional[int] = ..., group: Optional[int] = ..., request_id: Optional[int] = ...) -> None: ...

class RequestRayCast(_message.Message):
    __slots__ = ["mask", "request_id", "to"]
    FROM_FIELD_NUMBER: ClassVar[int]
    MASK_FIELD_NUMBER: ClassVar[int]
    REQUEST_ID_FIELD_NUMBER: ClassVar[int]
    TO_FIELD_NUMBER: ClassVar[int]
    mask: int
    request_id: int
    to: _ddf_math_pb2.Point3
    def __init__(self, to: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., mask: Optional[int] = ..., request_id: Optional[int] = ..., **kwargs) -> None: ...

class RequestVelocity(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SetGridShapeHull(_message.Message):
    __slots__ = ["column", "flip_horizontal", "flip_vertical", "hull", "rotate90", "row", "shape"]
    COLUMN_FIELD_NUMBER: ClassVar[int]
    FLIP_HORIZONTAL_FIELD_NUMBER: ClassVar[int]
    FLIP_VERTICAL_FIELD_NUMBER: ClassVar[int]
    HULL_FIELD_NUMBER: ClassVar[int]
    ROTATE90_FIELD_NUMBER: ClassVar[int]
    ROW_FIELD_NUMBER: ClassVar[int]
    SHAPE_FIELD_NUMBER: ClassVar[int]
    column: int
    flip_horizontal: int
    flip_vertical: int
    hull: int
    rotate90: int
    row: int
    shape: int
    def __init__(self, shape: Optional[int] = ..., row: Optional[int] = ..., column: Optional[int] = ..., hull: Optional[int] = ..., flip_horizontal: Optional[int] = ..., flip_vertical: Optional[int] = ..., rotate90: Optional[int] = ...) -> None: ...

class Trigger(_message.Message):
    __slots__ = ["group", "id"]
    GROUP_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    group: int
    id: int
    def __init__(self, id: Optional[int] = ..., group: Optional[int] = ...) -> None: ...

class TriggerEvent(_message.Message):
    __slots__ = ["a", "b", "enter"]
    A_FIELD_NUMBER: ClassVar[int]
    B_FIELD_NUMBER: ClassVar[int]
    ENTER_FIELD_NUMBER: ClassVar[int]
    a: Trigger
    b: Trigger
    enter: bool
    def __init__(self, enter: bool = ..., a: Optional[Union[Trigger, Mapping]] = ..., b: Optional[Union[Trigger, Mapping]] = ...) -> None: ...

class TriggerResponse(_message.Message):
    __slots__ = ["enter", "group", "other_group", "other_id", "own_group"]
    ENTER_FIELD_NUMBER: ClassVar[int]
    GROUP_FIELD_NUMBER: ClassVar[int]
    OTHER_GROUP_FIELD_NUMBER: ClassVar[int]
    OTHER_ID_FIELD_NUMBER: ClassVar[int]
    OWN_GROUP_FIELD_NUMBER: ClassVar[int]
    enter: bool
    group: int
    other_group: int
    other_id: int
    own_group: int
    def __init__(self, other_id: Optional[int] = ..., enter: bool = ..., group: Optional[int] = ..., other_group: Optional[int] = ..., own_group: Optional[int] = ...) -> None: ...

class VelocityResponse(_message.Message):
    __slots__ = ["angular_velocity", "linear_velocity"]
    ANGULAR_VELOCITY_FIELD_NUMBER: ClassVar[int]
    LINEAR_VELOCITY_FIELD_NUMBER: ClassVar[int]
    angular_velocity: _ddf_math_pb2.Vector3
    linear_velocity: _ddf_math_pb2.Vector3
    def __init__(self, linear_velocity: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ..., angular_velocity: Optional[Union[_ddf_math_pb2.Vector3, Mapping]] = ...) -> None: ...

class CollisionObjectType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
