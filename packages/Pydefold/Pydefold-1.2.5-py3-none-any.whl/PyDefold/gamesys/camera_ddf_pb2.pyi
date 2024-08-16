from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Optional

DESCRIPTOR: _descriptor.FileDescriptor

class AcquireCameraFocus(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class CameraDesc(_message.Message):
    __slots__ = ["aspect_ratio", "auto_aspect_ratio", "far_z", "fov", "near_z", "orthographic_projection", "orthographic_zoom"]
    ASPECT_RATIO_FIELD_NUMBER: ClassVar[int]
    AUTO_ASPECT_RATIO_FIELD_NUMBER: ClassVar[int]
    FAR_Z_FIELD_NUMBER: ClassVar[int]
    FOV_FIELD_NUMBER: ClassVar[int]
    NEAR_Z_FIELD_NUMBER: ClassVar[int]
    ORTHOGRAPHIC_PROJECTION_FIELD_NUMBER: ClassVar[int]
    ORTHOGRAPHIC_ZOOM_FIELD_NUMBER: ClassVar[int]
    aspect_ratio: float
    auto_aspect_ratio: int
    far_z: float
    fov: float
    near_z: float
    orthographic_projection: int
    orthographic_zoom: float
    def __init__(self, aspect_ratio: Optional[float] = ..., fov: Optional[float] = ..., near_z: Optional[float] = ..., far_z: Optional[float] = ..., auto_aspect_ratio: Optional[int] = ..., orthographic_projection: Optional[int] = ..., orthographic_zoom: Optional[float] = ...) -> None: ...

class ReleaseCameraFocus(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class SetCamera(_message.Message):
    __slots__ = ["aspect_ratio", "far_z", "fov", "near_z", "orthographic_projection", "orthographic_zoom"]
    ASPECT_RATIO_FIELD_NUMBER: ClassVar[int]
    FAR_Z_FIELD_NUMBER: ClassVar[int]
    FOV_FIELD_NUMBER: ClassVar[int]
    NEAR_Z_FIELD_NUMBER: ClassVar[int]
    ORTHOGRAPHIC_PROJECTION_FIELD_NUMBER: ClassVar[int]
    ORTHOGRAPHIC_ZOOM_FIELD_NUMBER: ClassVar[int]
    aspect_ratio: float
    far_z: float
    fov: float
    near_z: float
    orthographic_projection: int
    orthographic_zoom: float
    def __init__(self, aspect_ratio: Optional[float] = ..., fov: Optional[float] = ..., near_z: Optional[float] = ..., far_z: Optional[float] = ..., orthographic_projection: Optional[int] = ..., orthographic_zoom: Optional[float] = ...) -> None: ...
