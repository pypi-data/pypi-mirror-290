from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from gameobject import properties_ddf_pb2 as _properties_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
PROPERTY_TYPE_BOOLEAN: PropertyType
PROPERTY_TYPE_COUNT: PropertyType
PROPERTY_TYPE_HASH: PropertyType
PROPERTY_TYPE_MATRIX4: PropertyType
PROPERTY_TYPE_NUMBER: PropertyType
PROPERTY_TYPE_QUAT: PropertyType
PROPERTY_TYPE_URL: PropertyType
PROPERTY_TYPE_VECTOR3: PropertyType
PROPERTY_TYPE_VECTOR4: PropertyType

class AcquireInputFocus(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CollectionDesc(_message.Message):
    __slots__ = ["collection_instances", "component_types", "embedded_instances", "instances", "name", "property_resources", "scale_along_z"]
    COLLECTION_INSTANCES_FIELD_NUMBER: ClassVar[int]
    COMPONENT_TYPES_FIELD_NUMBER: ClassVar[int]
    EMBEDDED_INSTANCES_FIELD_NUMBER: ClassVar[int]
    INSTANCES_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    PROPERTY_RESOURCES_FIELD_NUMBER: ClassVar[int]
    SCALE_ALONG_Z_FIELD_NUMBER: ClassVar[int]
    collection_instances: _containers.RepeatedCompositeFieldContainer[CollectionInstanceDesc]
    component_types: _containers.RepeatedCompositeFieldContainer[ComponenTypeDesc]
    embedded_instances: _containers.RepeatedCompositeFieldContainer[EmbeddedInstanceDesc]
    instances: _containers.RepeatedCompositeFieldContainer[InstanceDesc]
    name: str
    property_resources: _containers.RepeatedScalarFieldContainer[str]
    scale_along_z: int
    def __init__(self, name: Optional[str] = ..., instances: Optional[Iterable[Union[InstanceDesc, Mapping]]] = ..., collection_instances: Optional[Iterable[Union[CollectionInstanceDesc, Mapping]]] = ..., scale_along_z: Optional[int] = ..., embedded_instances: Optional[Iterable[Union[EmbeddedInstanceDesc, Mapping]]] = ..., property_resources: Optional[Iterable[str]] = ..., component_types: Optional[Iterable[Union[ComponenTypeDesc, Mapping]]] = ...) -> None: ...

class CollectionInstanceDesc(_message.Message):
    __slots__ = ["collection", "id", "instance_properties", "position", "rotation", "scale", "scale3"]
    COLLECTION_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INSTANCE_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE3_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    collection: str
    id: str
    instance_properties: _containers.RepeatedCompositeFieldContainer[InstancePropertyDesc]
    position: _ddf_math_pb2.Point3
    rotation: _ddf_math_pb2.Quat
    scale: float
    scale3: _ddf_math_pb2.Vector3One
    def __init__(self, id: Optional[str] = ..., collection: Optional[str] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., scale: Optional[float] = ..., scale3: Optional[Union[_ddf_math_pb2.Vector3One, Mapping]] = ..., instance_properties: Optional[Iterable[Union[InstancePropertyDesc, Mapping]]] = ...) -> None: ...

class ComponenTypeDesc(_message.Message):
    __slots__ = ["max_count", "name_hash"]
    MAX_COUNT_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    max_count: int
    name_hash: int
    def __init__(self, name_hash: Optional[int] = ..., max_count: Optional[int] = ...) -> None: ...

class ComponentDesc(_message.Message):
    __slots__ = ["component", "id", "position", "properties", "property_decls", "rotation", "scale"]
    COMPONENT_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    PROPERTY_DECLS_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    component: str
    id: str
    position: _ddf_math_pb2.Point3
    properties: _containers.RepeatedCompositeFieldContainer[PropertyDesc]
    property_decls: _properties_ddf_pb2.PropertyDeclarations
    rotation: _ddf_math_pb2.Quat
    scale: _ddf_math_pb2.Vector3One
    def __init__(self, id: Optional[str] = ..., component: Optional[str] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., properties: Optional[Iterable[Union[PropertyDesc, Mapping]]] = ..., property_decls: Optional[Union[_properties_ddf_pb2.PropertyDeclarations, Mapping]] = ..., scale: Optional[Union[_ddf_math_pb2.Vector3One, Mapping]] = ...) -> None: ...

class ComponentPropertyDesc(_message.Message):
    __slots__ = ["id", "properties", "property_decls"]
    ID_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    PROPERTY_DECLS_FIELD_NUMBER: ClassVar[int]
    id: str
    properties: _containers.RepeatedCompositeFieldContainer[PropertyDesc]
    property_decls: _properties_ddf_pb2.PropertyDeclarations
    def __init__(self, id: Optional[str] = ..., properties: Optional[Iterable[Union[PropertyDesc, Mapping]]] = ..., property_decls: Optional[Union[_properties_ddf_pb2.PropertyDeclarations, Mapping]] = ...) -> None: ...

class Disable(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class EmbeddedComponentDesc(_message.Message):
    __slots__ = ["data", "id", "position", "rotation", "scale", "type"]
    DATA_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    data: str
    id: str
    position: _ddf_math_pb2.Point3
    rotation: _ddf_math_pb2.Quat
    scale: _ddf_math_pb2.Vector3One
    type: str
    def __init__(self, id: Optional[str] = ..., type: Optional[str] = ..., data: Optional[str] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., scale: Optional[Union[_ddf_math_pb2.Vector3One, Mapping]] = ...) -> None: ...

class EmbeddedInstanceDesc(_message.Message):
    __slots__ = ["children", "component_properties", "data", "id", "position", "rotation", "scale", "scale3"]
    CHILDREN_FIELD_NUMBER: ClassVar[int]
    COMPONENT_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    DATA_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE3_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    children: _containers.RepeatedScalarFieldContainer[str]
    component_properties: _containers.RepeatedCompositeFieldContainer[ComponentPropertyDesc]
    data: str
    id: str
    position: _ddf_math_pb2.Point3
    rotation: _ddf_math_pb2.Quat
    scale: float
    scale3: _ddf_math_pb2.Vector3One
    def __init__(self, id: Optional[str] = ..., children: Optional[Iterable[str]] = ..., data: Optional[str] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., component_properties: Optional[Iterable[Union[ComponentPropertyDesc, Mapping]]] = ..., scale: Optional[float] = ..., scale3: Optional[Union[_ddf_math_pb2.Vector3One, Mapping]] = ...) -> None: ...

class Enable(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class InstanceDesc(_message.Message):
    __slots__ = ["children", "component_properties", "id", "position", "prototype", "rotation", "scale", "scale3"]
    CHILDREN_FIELD_NUMBER: ClassVar[int]
    COMPONENT_PROPERTIES_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    PROTOTYPE_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE3_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    children: _containers.RepeatedScalarFieldContainer[str]
    component_properties: _containers.RepeatedCompositeFieldContainer[ComponentPropertyDesc]
    id: str
    position: _ddf_math_pb2.Point3
    prototype: str
    rotation: _ddf_math_pb2.Quat
    scale: float
    scale3: _ddf_math_pb2.Vector3One
    def __init__(self, id: Optional[str] = ..., prototype: Optional[str] = ..., children: Optional[Iterable[str]] = ..., position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Quat, Mapping]] = ..., component_properties: Optional[Iterable[Union[ComponentPropertyDesc, Mapping]]] = ..., scale: Optional[float] = ..., scale3: Optional[Union[_ddf_math_pb2.Vector3One, Mapping]] = ...) -> None: ...

class InstancePropertyDesc(_message.Message):
    __slots__ = ["id", "properties"]
    ID_FIELD_NUMBER: ClassVar[int]
    PROPERTIES_FIELD_NUMBER: ClassVar[int]
    id: str
    properties: _containers.RepeatedCompositeFieldContainer[ComponentPropertyDesc]
    def __init__(self, id: Optional[str] = ..., properties: Optional[Iterable[Union[ComponentPropertyDesc, Mapping]]] = ...) -> None: ...

class PropertyDesc(_message.Message):
    __slots__ = ["id", "type", "value"]
    ID_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    id: str
    type: PropertyType
    value: str
    def __init__(self, id: Optional[str] = ..., value: Optional[str] = ..., type: Optional[Union[PropertyType, str]] = ...) -> None: ...

class PrototypeDesc(_message.Message):
    __slots__ = ["components", "embedded_components", "property_resources"]
    COMPONENTS_FIELD_NUMBER: ClassVar[int]
    EMBEDDED_COMPONENTS_FIELD_NUMBER: ClassVar[int]
    PROPERTY_RESOURCES_FIELD_NUMBER: ClassVar[int]
    components: _containers.RepeatedCompositeFieldContainer[ComponentDesc]
    embedded_components: _containers.RepeatedCompositeFieldContainer[EmbeddedComponentDesc]
    property_resources: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, components: Optional[Iterable[Union[ComponentDesc, Mapping]]] = ..., embedded_components: Optional[Iterable[Union[EmbeddedComponentDesc, Mapping]]] = ..., property_resources: Optional[Iterable[str]] = ...) -> None: ...

class ReleaseInputFocus(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class ScriptMessage(_message.Message):
    __slots__ = ["descriptor_hash", "function", "payload_size", "unref_function"]
    DESCRIPTOR_HASH_FIELD_NUMBER: ClassVar[int]
    FUNCTION_FIELD_NUMBER: ClassVar[int]
    PAYLOAD_SIZE_FIELD_NUMBER: ClassVar[int]
    UNREF_FUNCTION_FIELD_NUMBER: ClassVar[int]
    descriptor_hash: int
    function: int
    payload_size: int
    unref_function: bool
    def __init__(self, descriptor_hash: Optional[int] = ..., payload_size: Optional[int] = ..., function: Optional[int] = ..., unref_function: bool = ...) -> None: ...

class ScriptUnrefMessage(_message.Message):
    __slots__ = ["reference"]
    REFERENCE_FIELD_NUMBER: ClassVar[int]
    reference: int
    def __init__(self, reference: Optional[int] = ...) -> None: ...

class SetParent(_message.Message):
    __slots__ = ["keep_world_transform", "parent_id"]
    KEEP_WORLD_TRANSFORM_FIELD_NUMBER: ClassVar[int]
    PARENT_ID_FIELD_NUMBER: ClassVar[int]
    keep_world_transform: int
    parent_id: int
    def __init__(self, parent_id: Optional[int] = ..., keep_world_transform: Optional[int] = ...) -> None: ...

class PropertyType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
