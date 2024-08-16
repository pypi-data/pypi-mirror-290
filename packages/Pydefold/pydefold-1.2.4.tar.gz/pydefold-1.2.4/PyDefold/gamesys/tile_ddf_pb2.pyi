from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
PLAYBACK_LOOP_BACKWARD: Playback
PLAYBACK_LOOP_FORWARD: Playback
PLAYBACK_LOOP_PINGPONG: Playback
PLAYBACK_NONE: Playback
PLAYBACK_ONCE_BACKWARD: Playback
PLAYBACK_ONCE_FORWARD: Playback
PLAYBACK_ONCE_PINGPONG: Playback
SPRITE_TRIM_MODE_4: SpriteTrimmingMode
SPRITE_TRIM_MODE_5: SpriteTrimmingMode
SPRITE_TRIM_MODE_6: SpriteTrimmingMode
SPRITE_TRIM_MODE_7: SpriteTrimmingMode
SPRITE_TRIM_MODE_8: SpriteTrimmingMode
SPRITE_TRIM_MODE_OFF: SpriteTrimmingMode
SPRITE_TRIM_POLYGONS: SpriteTrimmingMode

class Animation(_message.Message):
    __slots__ = ["cues", "end_tile", "flip_horizontal", "flip_vertical", "fps", "id", "playback", "start_tile"]
    CUES_FIELD_NUMBER: ClassVar[int]
    END_TILE_FIELD_NUMBER: ClassVar[int]
    FLIP_HORIZONTAL_FIELD_NUMBER: ClassVar[int]
    FLIP_VERTICAL_FIELD_NUMBER: ClassVar[int]
    FPS_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    PLAYBACK_FIELD_NUMBER: ClassVar[int]
    START_TILE_FIELD_NUMBER: ClassVar[int]
    cues: _containers.RepeatedCompositeFieldContainer[Cue]
    end_tile: int
    flip_horizontal: int
    flip_vertical: int
    fps: int
    id: str
    playback: Playback
    start_tile: int
    def __init__(self, id: Optional[str] = ..., start_tile: Optional[int] = ..., end_tile: Optional[int] = ..., playback: Optional[Union[Playback, str]] = ..., fps: Optional[int] = ..., flip_horizontal: Optional[int] = ..., flip_vertical: Optional[int] = ..., cues: Optional[Iterable[Union[Cue, Mapping]]] = ...) -> None: ...

class ConvexHull(_message.Message):
    __slots__ = ["collision_group", "count", "index"]
    COLLISION_GROUP_FIELD_NUMBER: ClassVar[int]
    COUNT_FIELD_NUMBER: ClassVar[int]
    INDEX_FIELD_NUMBER: ClassVar[int]
    collision_group: str
    count: int
    index: int
    def __init__(self, index: Optional[int] = ..., count: Optional[int] = ..., collision_group: Optional[str] = ...) -> None: ...

class Cue(_message.Message):
    __slots__ = ["frame", "id", "value"]
    FRAME_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    frame: int
    id: str
    value: float
    def __init__(self, id: Optional[str] = ..., frame: Optional[int] = ..., value: Optional[float] = ...) -> None: ...

class ResetConstantTileMap(_message.Message):
    __slots__ = ["name_hash"]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    name_hash: int
    def __init__(self, name_hash: Optional[int] = ...) -> None: ...

class SetConstantTileMap(_message.Message):
    __slots__ = ["name_hash", "value"]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    VALUE_FIELD_NUMBER: ClassVar[int]
    name_hash: int
    value: _ddf_math_pb2.Vector4
    def __init__(self, name_hash: Optional[int] = ..., value: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ...) -> None: ...

class TileCell(_message.Message):
    __slots__ = ["h_flip", "rotate90", "tile", "v_flip", "x", "y"]
    H_FLIP_FIELD_NUMBER: ClassVar[int]
    ROTATE90_FIELD_NUMBER: ClassVar[int]
    TILE_FIELD_NUMBER: ClassVar[int]
    V_FLIP_FIELD_NUMBER: ClassVar[int]
    X_FIELD_NUMBER: ClassVar[int]
    Y_FIELD_NUMBER: ClassVar[int]
    h_flip: int
    rotate90: int
    tile: int
    v_flip: int
    x: int
    y: int
    def __init__(self, x: Optional[int] = ..., y: Optional[int] = ..., tile: Optional[int] = ..., h_flip: Optional[int] = ..., v_flip: Optional[int] = ..., rotate90: Optional[int] = ...) -> None: ...

class TileGrid(_message.Message):
    __slots__ = ["blend_mode", "layers", "material", "tile_set"]
    class BlendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BLEND_MODE_ADD: TileGrid.BlendMode
    BLEND_MODE_ADD_ALPHA: TileGrid.BlendMode
    BLEND_MODE_ALPHA: TileGrid.BlendMode
    BLEND_MODE_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_MULT: TileGrid.BlendMode
    BLEND_MODE_SCREEN: TileGrid.BlendMode
    LAYERS_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    TILE_SET_FIELD_NUMBER: ClassVar[int]
    blend_mode: TileGrid.BlendMode
    layers: _containers.RepeatedCompositeFieldContainer[TileLayer]
    material: str
    tile_set: str
    def __init__(self, tile_set: Optional[str] = ..., layers: Optional[Iterable[Union[TileLayer, Mapping]]] = ..., material: Optional[str] = ..., blend_mode: Optional[Union[TileGrid.BlendMode, str]] = ...) -> None: ...

class TileLayer(_message.Message):
    __slots__ = ["cell", "id", "id_hash", "is_visible", "z"]
    CELL_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    ID_HASH_FIELD_NUMBER: ClassVar[int]
    IS_VISIBLE_FIELD_NUMBER: ClassVar[int]
    Z_FIELD_NUMBER: ClassVar[int]
    cell: _containers.RepeatedCompositeFieldContainer[TileCell]
    id: str
    id_hash: int
    is_visible: int
    z: float
    def __init__(self, id: Optional[str] = ..., z: Optional[float] = ..., is_visible: Optional[int] = ..., id_hash: Optional[int] = ..., cell: Optional[Iterable[Union[TileCell, Mapping]]] = ...) -> None: ...

class TileSet(_message.Message):
    __slots__ = ["animations", "collision", "collision_groups", "convex_hull_points", "convex_hulls", "extrude_borders", "image", "inner_padding", "material_tag", "sprite_trim_mode", "tile_height", "tile_margin", "tile_spacing", "tile_width"]
    ANIMATIONS_FIELD_NUMBER: ClassVar[int]
    COLLISION_FIELD_NUMBER: ClassVar[int]
    COLLISION_GROUPS_FIELD_NUMBER: ClassVar[int]
    CONVEX_HULLS_FIELD_NUMBER: ClassVar[int]
    CONVEX_HULL_POINTS_FIELD_NUMBER: ClassVar[int]
    EXTRUDE_BORDERS_FIELD_NUMBER: ClassVar[int]
    IMAGE_FIELD_NUMBER: ClassVar[int]
    INNER_PADDING_FIELD_NUMBER: ClassVar[int]
    MATERIAL_TAG_FIELD_NUMBER: ClassVar[int]
    SPRITE_TRIM_MODE_FIELD_NUMBER: ClassVar[int]
    TILE_HEIGHT_FIELD_NUMBER: ClassVar[int]
    TILE_MARGIN_FIELD_NUMBER: ClassVar[int]
    TILE_SPACING_FIELD_NUMBER: ClassVar[int]
    TILE_WIDTH_FIELD_NUMBER: ClassVar[int]
    animations: _containers.RepeatedCompositeFieldContainer[Animation]
    collision: str
    collision_groups: _containers.RepeatedScalarFieldContainer[str]
    convex_hull_points: _containers.RepeatedScalarFieldContainer[float]
    convex_hulls: _containers.RepeatedCompositeFieldContainer[ConvexHull]
    extrude_borders: int
    image: str
    inner_padding: int
    material_tag: str
    sprite_trim_mode: SpriteTrimmingMode
    tile_height: int
    tile_margin: int
    tile_spacing: int
    tile_width: int
    def __init__(self, image: Optional[str] = ..., tile_width: Optional[int] = ..., tile_height: Optional[int] = ..., tile_margin: Optional[int] = ..., tile_spacing: Optional[int] = ..., collision: Optional[str] = ..., material_tag: Optional[str] = ..., convex_hulls: Optional[Iterable[Union[ConvexHull, Mapping]]] = ..., convex_hull_points: Optional[Iterable[float]] = ..., collision_groups: Optional[Iterable[str]] = ..., animations: Optional[Iterable[Union[Animation, Mapping]]] = ..., extrude_borders: Optional[int] = ..., inner_padding: Optional[int] = ..., sprite_trim_mode: Optional[Union[SpriteTrimmingMode, str]] = ...) -> None: ...

class Playback(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class SpriteTrimmingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
