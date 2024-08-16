from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from gamesys import tile_ddf_pb2 as _tile_ddf_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class SpriteGeometry(_message.Message):
    __slots__ = ["center_x", "center_y", "height", "indices", "rotated", "trim_mode", "uvs", "vertices", "width"]
    CENTER_X_FIELD_NUMBER: ClassVar[int]
    CENTER_Y_FIELD_NUMBER: ClassVar[int]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    INDICES_FIELD_NUMBER: ClassVar[int]
    ROTATED_FIELD_NUMBER: ClassVar[int]
    TRIM_MODE_FIELD_NUMBER: ClassVar[int]
    UVS_FIELD_NUMBER: ClassVar[int]
    VERTICES_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    center_x: float
    center_y: float
    height: int
    indices: _containers.RepeatedScalarFieldContainer[int]
    rotated: bool
    trim_mode: _tile_ddf_pb2.SpriteTrimmingMode
    uvs: _containers.RepeatedScalarFieldContainer[float]
    vertices: _containers.RepeatedScalarFieldContainer[float]
    width: int
    def __init__(self, width: Optional[int] = ..., height: Optional[int] = ..., center_x: Optional[float] = ..., center_y: Optional[float] = ..., rotated: bool = ..., trim_mode: Optional[Union[_tile_ddf_pb2.SpriteTrimmingMode, str]] = ..., vertices: Optional[Iterable[float]] = ..., uvs: Optional[Iterable[float]] = ..., indices: Optional[Iterable[int]] = ...) -> None: ...

class TextureSet(_message.Message):
    __slots__ = ["animations", "collision_groups", "collision_hull_points", "convex_hulls", "frame_indices", "geometries", "height", "image_name_hashes", "page_count", "page_indices", "tex_coords", "tex_dims", "texture", "texture_hash", "tile_count", "tile_height", "tile_width", "use_geometries", "width"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    COLLISION_GROUPS_FIELD_NUMBER: ClassVar[int]
    COLLISION_HULL_POINTS_FIELD_NUMBER: ClassVar[int]
    CONVEX_HULLS_FIELD_NUMBER: ClassVar[int]
    FRAME_INDICES_FIELD_NUMBER: ClassVar[int]
    GEOMETRIES_FIELD_NUMBER: ClassVar[int]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    IMAGE_NAME_HASHES_FIELD_NUMBER: ClassVar[int]
    PAGE_COUNT_FIELD_NUMBER: ClassVar[int]
    PAGE_INDICES_FIELD_NUMBER: ClassVar[int]
    TEXTURE_FIELD_NUMBER: ClassVar[int]
    TEXTURE_HASH_FIELD_NUMBER: ClassVar[int]
    TEX_COORDS_FIELD_NUMBER: ClassVar[int]
    TEX_DIMS_FIELD_NUMBER: ClassVar[int]
    TILE_COUNT_FIELD_NUMBER: ClassVar[int]
    TILE_HEIGHT_FIELD_NUMBER: ClassVar[int]
    TILE_WIDTH_FIELD_NUMBER: ClassVar[int]
    USE_GEOMETRIES_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    animations: _containers.RepeatedCompositeFieldContainer[TextureSetAnimation]
    collision_groups: _containers.RepeatedScalarFieldContainer[str]
    collision_hull_points: _containers.RepeatedScalarFieldContainer[float]
    convex_hulls: _containers.RepeatedCompositeFieldContainer[_tile_ddf_pb2.ConvexHull]
    frame_indices: _containers.RepeatedScalarFieldContainer[int]
    geometries: _containers.RepeatedCompositeFieldContainer[SpriteGeometry]
    height: int
    image_name_hashes: _containers.RepeatedScalarFieldContainer[int]
    page_count: int
    page_indices: _containers.RepeatedScalarFieldContainer[int]
    tex_coords: bytes
    tex_dims: bytes
    texture: str
    texture_hash: int
    tile_count: int
    tile_height: int
    tile_width: int
    use_geometries: int
    width: int
    def __init__(self, texture: Optional[str] = ..., width: Optional[int] = ..., height: Optional[int] = ..., texture_hash: Optional[int] = ..., animations: Optional[Iterable[Union[TextureSetAnimation, Mapping]]] = ..., tile_width: Optional[int] = ..., tile_height: Optional[int] = ..., tile_count: Optional[int] = ..., collision_hull_points: Optional[Iterable[float]] = ..., collision_groups: Optional[Iterable[str]] = ..., convex_hulls: Optional[Iterable[Union[_tile_ddf_pb2.ConvexHull, Mapping]]] = ..., image_name_hashes: Optional[Iterable[int]] = ..., frame_indices: Optional[Iterable[int]] = ..., tex_coords: Optional[bytes] = ..., tex_dims: Optional[bytes] = ..., geometries: Optional[Iterable[Union[SpriteGeometry, Mapping]]] = ..., use_geometries: Optional[int] = ..., page_indices: Optional[Iterable[int]] = ..., page_count: Optional[int] = ...) -> None: ...

class TextureSetAnimation(_message.Message):
    __slots__ = ["end", "flip_horizontal", "flip_vertical", "fps", "height", "id", "playback", "start", "width"]
    END_FIELD_NUMBER: ClassVar[int]
    FLIP_HORIZONTAL_FIELD_NUMBER: ClassVar[int]
    FLIP_VERTICAL_FIELD_NUMBER: ClassVar[int]
    FPS_FIELD_NUMBER: ClassVar[int]
    HEIGHT_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_FIELD_NUMBER: ClassVar[int]
    START_FIELD_NUMBER: ClassVar[int]
    WIDTH_FIELD_NUMBER: ClassVar[int]
    end: int
    flip_horizontal: int
    flip_vertical: int
    fps: int
    height: int
    id: str
    playback: _tile_ddf_pb2.Playback
    start: int
    width: int
    def __init__(self, id: Optional[str] = ..., width: Optional[int] = ..., height: Optional[int] = ..., start: Optional[int] = ..., end: Optional[int] = ..., fps: Optional[int] = ..., playback: Optional[Union[_tile_ddf_pb2.Playback, str]] = ..., flip_horizontal: Optional[int] = ..., flip_vertical: Optional[int] = ...) -> None: ...
