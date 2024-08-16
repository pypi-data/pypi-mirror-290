from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LabelDesc(_message.Message):
    __slots__ = ["blend_mode", "color", "font", "leading", "line_break", "material", "outline", "pivot", "scale", "shadow", "size", "text", "tracking"]
    class BlendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Pivot(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BLEND_MODE_ADD: LabelDesc.BlendMode
    BLEND_MODE_ALPHA: LabelDesc.BlendMode
    BLEND_MODE_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_MULT: LabelDesc.BlendMode
    BLEND_MODE_SCREEN: LabelDesc.BlendMode
    COLOR_FIELD_NUMBER: ClassVar[int]
    FONT_FIELD_NUMBER: ClassVar[int]
    LEADING_FIELD_NUMBER: ClassVar[int]
    LINE_BREAK_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    OUTLINE_FIELD_NUMBER: ClassVar[int]
    PIVOT_CENTER: LabelDesc.Pivot
    PIVOT_E: LabelDesc.Pivot
    PIVOT_FIELD_NUMBER: ClassVar[int]
    PIVOT_N: LabelDesc.Pivot
    PIVOT_NE: LabelDesc.Pivot
    PIVOT_NW: LabelDesc.Pivot
    PIVOT_S: LabelDesc.Pivot
    PIVOT_SE: LabelDesc.Pivot
    PIVOT_SW: LabelDesc.Pivot
    PIVOT_W: LabelDesc.Pivot
    SCALE_FIELD_NUMBER: ClassVar[int]
    SHADOW_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    TRACKING_FIELD_NUMBER: ClassVar[int]
    blend_mode: LabelDesc.BlendMode
    color: _ddf_math_pb2.Vector4One
    font: str
    leading: float
    line_break: bool
    material: str
    outline: _ddf_math_pb2.Vector4WOne
    pivot: LabelDesc.Pivot
    scale: _ddf_math_pb2.Vector4One
    shadow: _ddf_math_pb2.Vector4WOne
    size: _ddf_math_pb2.Vector4
    text: str
    tracking: float
    def __init__(self, size: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., scale: Optional[Union[_ddf_math_pb2.Vector4One, Mapping]] = ..., color: Optional[Union[_ddf_math_pb2.Vector4One, Mapping]] = ..., outline: Optional[Union[_ddf_math_pb2.Vector4WOne, Mapping]] = ..., shadow: Optional[Union[_ddf_math_pb2.Vector4WOne, Mapping]] = ..., leading: Optional[float] = ..., tracking: Optional[float] = ..., pivot: Optional[Union[LabelDesc.Pivot, str]] = ..., blend_mode: Optional[Union[LabelDesc.BlendMode, str]] = ..., line_break: bool = ..., text: Optional[str] = ..., font: Optional[str] = ..., material: Optional[str] = ...) -> None: ...

class SetText(_message.Message):
    __slots__ = ["text"]
    TEXT_FIELD_NUMBER: ClassVar[int]
    text: str
    def __init__(self, text: Optional[str] = ...) -> None: ...
