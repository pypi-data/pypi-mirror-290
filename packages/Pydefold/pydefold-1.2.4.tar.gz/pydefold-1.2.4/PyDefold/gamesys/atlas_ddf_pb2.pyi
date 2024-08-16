from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from gamesys import tile_ddf_pb2 as _tile_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class Atlas(_message.Message):
    __slots__ = ["animations", "extrude_borders", "images", "inner_padding", "margin", "max_page_height", "max_page_width", "rename_patterns"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    EXTRUDE_BORDERS_FIELD_NUMBER: ClassVar[int]
    IMAGES_FIELD_NUMBER: ClassVar[int]
    INNER_PADDING_FIELD_NUMBER: ClassVar[int]
    MARGIN_FIELD_NUMBER: ClassVar[int]
    MAX_PAGE_HEIGHT_FIELD_NUMBER: ClassVar[int]
    MAX_PAGE_WIDTH_FIELD_NUMBER: ClassVar[int]
    RENAME_PATTERNS_FIELD_NUMBER: ClassVar[int]
    animations: _containers.RepeatedCompositeFieldContainer[AtlasAnimation]
    extrude_borders: int
    images: _containers.RepeatedCompositeFieldContainer[AtlasImage]
    inner_padding: int
    margin: int
    max_page_height: int
    max_page_width: int
    rename_patterns: str
    def __init__(self, images: Optional[Iterable[Union[AtlasImage, Mapping]]] = ..., animations: Optional[Iterable[Union[AtlasAnimation, Mapping]]] = ..., margin: Optional[int] = ..., extrude_borders: Optional[int] = ..., inner_padding: Optional[int] = ..., max_page_width: Optional[int] = ..., max_page_height: Optional[int] = ..., rename_patterns: Optional[str] = ...) -> None: ...

class AtlasAnimation(_message.Message):
    __slots__ = ["flip_horizontal", "flip_vertical", "fps", "id", "images", "playback"]
    FLIP_HORIZONTAL_FIELD_NUMBER: ClassVar[int]
    FLIP_VERTICAL_FIELD_NUMBER: ClassVar[int]
    FPS_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    IMAGES_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_FIELD_NUMBER: ClassVar[int]
    flip_horizontal: int
    flip_vertical: int
    fps: int
    id: str
    images: _containers.RepeatedCompositeFieldContainer[AtlasImage]
    playback: _tile_ddf_pb2.Playback
    def __init__(self, id: Optional[str] = ..., images: Optional[Iterable[Union[AtlasImage, Mapping]]] = ..., playback: Optional[Union[_tile_ddf_pb2.Playback, str]] = ..., fps: Optional[int] = ..., flip_horizontal: Optional[int] = ..., flip_vertical: Optional[int] = ...) -> None: ...

class AtlasImage(_message.Message):
    __slots__ = ["image", "sprite_trim_mode"]
    IMAGE_FIELD_NUMBER: ClassVar[int]
    SPRITE_TRIM_MODE_FIELD_NUMBER: ClassVar[int]
    image: str
    sprite_trim_mode: _tile_ddf_pb2.SpriteTrimmingMode
    def __init__(self, image: Optional[str] = ..., sprite_trim_mode: Optional[Union[_tile_ddf_pb2.SpriteTrimmingMode, str]] = ...) -> None: ...
