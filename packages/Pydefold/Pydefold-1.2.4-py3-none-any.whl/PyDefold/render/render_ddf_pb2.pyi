from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class ClearColor(_message.Message):
    __slots__ = ["color"]
    COLOR_FIELD_NUMBER: ClassVar[int]
    color: _ddf_math_pb2.Vector4
    def __init__(self, color: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ...) -> None: ...

class DisplayProfile(_message.Message):
    __slots__ = ["name", "qualifiers"]
    NAME_FIELD_NUMBER: ClassVar[int]
    QUALIFIERS_FIELD_NUMBER: ClassVar[int]
    name: str
    qualifiers: _containers.RepeatedCompositeFieldContainer[DisplayProfileQualifier]
    def __init__(self, name: Optional[str] = ..., qualifiers: Optional[Iterable[Union[DisplayProfileQualifier, Mapping]]] = ...) -> None: ...

class DisplayProfileQualifier(_message.Message):
    __slots__ = ["device_models", "height", "width"]
    DEVICE_MODELS_FIELD_NUMBER: ClassVar[int]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    device_models: _containers.RepeatedScalarFieldContainer[str]
    height: int
    width: int
    def __init__(self, width: Optional[int] = ..., height: Optional[int] = ..., device_models: Optional[Iterable[str]] = ...) -> None: ...

class DisplayProfiles(_message.Message):
    __slots__ = ["profiles"]
    PROFILES_FIELD_NUMBER: ClassVar[int]
    profiles: _containers.RepeatedCompositeFieldContainer[DisplayProfile]
    def __init__(self, profiles: Optional[Iterable[Union[DisplayProfile, Mapping]]] = ...) -> None: ...

class DrawDebugText(_message.Message):
    __slots__ = ["color", "position", "text"]
    COLOR_FIELD_NUMBER: ClassVar[int]
    POSITION_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    color: _ddf_math_pb2.Vector4
    position: _ddf_math_pb2.Point3
    text: str
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., text: Optional[str] = ..., color: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ...) -> None: ...

class DrawLine(_message.Message):
    __slots__ = ["color", "end_point", "start_point"]
    COLOR_FIELD_NUMBER: ClassVar[int]
    END_POINT_FIELD_NUMBER: ClassVar[int]
    START_POINT_FIELD_NUMBER: ClassVar[int]
    color: _ddf_math_pb2.Vector4
    end_point: _ddf_math_pb2.Point3
    start_point: _ddf_math_pb2.Point3
    def __init__(self, start_point: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., end_point: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., color: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ...) -> None: ...

class DrawText(_message.Message):
    __slots__ = ["position", "text"]
    POSITION_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    position: _ddf_math_pb2.Point3
    text: str
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Point3, Mapping]] = ..., text: Optional[str] = ...) -> None: ...

class RenderPrototypeDesc(_message.Message):
    __slots__ = ["materials", "render_resources", "script"]
    class MaterialDesc(_message.Message):
        __slots__ = ["material", "name"]
        MATERIAL_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        material: str
        name: str
        def __init__(self, name: Optional[str] = ..., material: Optional[str] = ...) -> None: ...
    class RenderResourceDesc(_message.Message):
        __slots__ = ["name", "path"]
        NAME_FIELD_NUMBER: ClassVar[int]
        PATH_FIELD_NUMBER: ClassVar[int]
        name: str
        path: str
        def __init__(self, name: Optional[str] = ..., path: Optional[str] = ...) -> None: ...
    MATERIALS_FIELD_NUMBER: ClassVar[int]
    RENDER_RESOURCES_FIELD_NUMBER: ClassVar[int]
    SCRIPT_FIELD_NUMBER: ClassVar[int]
    materials: _containers.RepeatedCompositeFieldContainer[RenderPrototypeDesc.MaterialDesc]
    render_resources: _containers.RepeatedCompositeFieldContainer[RenderPrototypeDesc.RenderResourceDesc]
    script: str
    def __init__(self, script: Optional[str] = ..., materials: Optional[Iterable[Union[RenderPrototypeDesc.MaterialDesc, Mapping]]] = ..., render_resources: Optional[Iterable[Union[RenderPrototypeDesc.RenderResourceDesc, Mapping]]] = ...) -> None: ...

class Resize(_message.Message):
    __slots__ = ["height", "width"]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    height: int
    width: int
    def __init__(self, width: Optional[int] = ..., height: Optional[int] = ...) -> None: ...

class WindowResized(_message.Message):
    __slots__ = ["height", "width"]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    height: int
    width: int
    def __init__(self, width: Optional[int] = ..., height: Optional[int] = ...) -> None: ...
