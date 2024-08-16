from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Matrix4(_message.Message):
    __slots__ = ["m00", "m01", "m02", "m03", "m10", "m11", "m12", "m13", "m20", "m21", "m22", "m23", "m30", "m31", "m32", "m33"]
    M00_FIELD_NUMBER: ClassVar[int]
    M01_FIELD_NUMBER: ClassVar[int]
    M02_FIELD_NUMBER: ClassVar[int]
    M03_FIELD_NUMBER: ClassVar[int]
    M10_FIELD_NUMBER: ClassVar[int]
    M11_FIELD_NUMBER: ClassVar[int]
    M12_FIELD_NUMBER: ClassVar[int]
    M13_FIELD_NUMBER: ClassVar[int]
    M20_FIELD_NUMBER: ClassVar[int]
    M21_FIELD_NUMBER: ClassVar[int]
    M22_FIELD_NUMBER: ClassVar[int]
    M23_FIELD_NUMBER: ClassVar[int]
    M30_FIELD_NUMBER: ClassVar[int]
    M31_FIELD_NUMBER: ClassVar[int]
    M32_FIELD_NUMBER: ClassVar[int]
    M33_FIELD_NUMBER: ClassVar[int]
    m00: float
    m01: float
    m02: float
    m03: float
    m10: float
    m11: float
    m12: float
    m13: float
    m20: float
    m21: float
    m22: float
    m23: float
    m30: float
    m31: float
    m32: float
    m33: float
    def __init__(self, m00: Optional[float] = ..., m01: Optional[float] = ..., m02: Optional[float] = ..., m03: Optional[float] = ..., m10: Optional[float] = ..., m11: Optional[float] = ..., m12: Optional[float] = ..., m13: Optional[float] = ..., m20: Optional[float] = ..., m21: Optional[float] = ..., m22: Optional[float] = ..., m23: Optional[float] = ..., m30: Optional[float] = ..., m31: Optional[float] = ..., m32: Optional[float] = ..., m33: Optional[float] = ...) -> None: ...

class Point3(_message.Message):
    __slots__ = ["d", "x", "y", "z"]
    D_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    d: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., d: Optional[float] = ...) -> None: ...

class Quat(_message.Message):
    __slots__ = ["w", "x", "y", "z"]
    W_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    w: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., w: Optional[float] = ...) -> None: ...

class Transform(_message.Message):
    __slots__ = ["rotation", "scale", "translation"]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    TRANSLATION_FIELD_NUMBER: ClassVar[int]
    rotation: Quat
    scale: Vector3
    translation: Vector3
    def __init__(self, rotation: Optional[Union[Quat, Mapping]] = ..., translation: Optional[Union[Vector3, Mapping]] = ..., scale: Optional[Union[Vector3, Mapping]] = ...) -> None: ...

class Vector3(_message.Message):
    __slots__ = ["d", "x", "y", "z"]
    D_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    d: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., d: Optional[float] = ...) -> None: ...

class Vector3One(_message.Message):
    __slots__ = ["d", "x", "y", "z"]
    D_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    d: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., d: Optional[float] = ...) -> None: ...

class Vector4(_message.Message):
    __slots__ = ["w", "x", "y", "z"]
    W_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    w: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., w: Optional[float] = ...) -> None: ...

class Vector4One(_message.Message):
    __slots__ = ["w", "x", "y", "z"]
    W_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    w: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., w: Optional[float] = ...) -> None: ...

class Vector4WOne(_message.Message):
    __slots__ = ["w", "x", "y", "z"]
    W_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    w: float
    x: float
    y: float
    z: float
    def __init__(self, x: Optional[float] = ..., y: Optional[float] = ..., z: Optional[float] = ..., w: Optional[float] = ...) -> None: ...
