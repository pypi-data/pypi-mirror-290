from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
MODE_MULTI_LAYER: FontRenderMode
MODE_SINGLE_LAYER: FontRenderMode
TYPE_BITMAP: FontTextureFormat
TYPE_DISTANCE_FIELD: FontTextureFormat

class FontDesc(_message.Message):
    __slots__ = ["all_chars", "alpha", "antialias", "cache_height", "cache_width", "characters", "extra_characters", "font", "material", "outline_alpha", "outline_width", "output_format", "render_mode", "shadow_alpha", "shadow_blur", "shadow_x", "shadow_y", "size"]
    ALL_CHARS_FIELD_NUMBER: ClassVar[int]
    ALPHA_FIELD_NUMBER: ClassVar[int]
    ANTIALIAS_FIELD_NUMBER: ClassVar[int]
    CACHE_HEIGHT_FIELD_NUMBER: ClassVar[int]
    CACHE_WIDTH_FIELD_NUMBER: ClassVar[int]
    CHARACTERS_FIELD_NUMBER: ClassVar[int]
    EXTRA_CHARACTERS_FIELD_NUMBER: ClassVar[int]
    FONT_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    OUTLINE_ALPHA_FIELD_NUMBER: ClassVar[int]
    OUTLINE_WIDTH_FIELD_NUMBER: ClassVar[int]
    OUTPUT_FORMAT_FIELD_NUMBER: ClassVar[int]
    RENDER_MODE_FIELD_NUMBER: ClassVar[int]
    SHADOW_ALPHA_FIELD_NUMBER: ClassVar[int]
    SHADOW_BLUR_FIELD_NUMBER: ClassVar[int]
    SHADOW_X_FIELD_NUMBER: ClassVar[int]
    SHADOW_Y_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    all_chars: bool
    alpha: float
    antialias: int
    cache_height: int
    cache_width: int
    characters: str
    extra_characters: str
    font: str
    material: str
    outline_alpha: float
    outline_width: float
    output_format: FontTextureFormat
    render_mode: FontRenderMode
    shadow_alpha: float
    shadow_blur: int
    shadow_x: float
    shadow_y: float
    size: int
    def __init__(self, font: Optional[str] = ..., material: Optional[str] = ..., size: Optional[int] = ..., antialias: Optional[int] = ..., alpha: Optional[float] = ..., outline_alpha: Optional[float] = ..., outline_width: Optional[float] = ..., shadow_alpha: Optional[float] = ..., shadow_blur: Optional[int] = ..., shadow_x: Optional[float] = ..., shadow_y: Optional[float] = ..., extra_characters: Optional[str] = ..., output_format: Optional[Union[FontTextureFormat, str]] = ..., all_chars: bool = ..., cache_width: Optional[int] = ..., cache_height: Optional[int] = ..., render_mode: Optional[Union[FontRenderMode, str]] = ..., characters: Optional[str] = ...) -> None: ...

class FontMap(_message.Message):
    __slots__ = ["alpha", "glyph_bank", "layer_mask", "material", "outline_alpha", "shadow_alpha", "shadow_x", "shadow_y"]
    ALPHA_FIELD_NUMBER: ClassVar[int]
    GLYPH_BANK_FIELD_NUMBER: ClassVar[int]
    LAYER_MASK_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    OUTLINE_ALPHA_FIELD_NUMBER: ClassVar[int]
    SHADOW_ALPHA_FIELD_NUMBER: ClassVar[int]
    SHADOW_X_FIELD_NUMBER: ClassVar[int]
    SHADOW_Y_FIELD_NUMBER: ClassVar[int]
    alpha: float
    glyph_bank: str
    layer_mask: int
    material: str
    outline_alpha: float
    shadow_alpha: float
    shadow_x: float
    shadow_y: float
    def __init__(self, glyph_bank: Optional[str] = ..., material: Optional[str] = ..., shadow_x: Optional[float] = ..., shadow_y: Optional[float] = ..., alpha: Optional[float] = ..., outline_alpha: Optional[float] = ..., shadow_alpha: Optional[float] = ..., layer_mask: Optional[int] = ...) -> None: ...

class GlyphBank(_message.Message):
    __slots__ = ["cache_cell_height", "cache_cell_max_ascent", "cache_cell_width", "cache_height", "cache_width", "glyph_channels", "glyph_data", "glyph_padding", "glyphs", "image_format", "is_monospaced", "max_ascent", "max_descent", "padding", "sdf_offset", "sdf_outline", "sdf_shadow", "sdf_spread"]
    class Glyph(_message.Message):
        __slots__ = ["advance", "ascent", "character", "descent", "glyph_data_offset", "glyph_data_size", "left_bearing", "width", "x", "y"]
        ADVANCE_FIELD_NUMBER: ClassVar[int]
        ASCENT_FIELD_NUMBER: ClassVar[int]
        CHARACTER_FIELD_NUMBER: ClassVar[int]
        DESCENT_FIELD_NUMBER: ClassVar[int]
        GLYPH_DATA_OFFSET_FIELD_NUMBER: ClassVar[int]
        GLYPH_DATA_SIZE_FIELD_NUMBER: ClassVar[int]
        LEFT_BEARING_FIELD_NUMBER: ClassVar[int]
        WIDTH_FIELD_NUMBER: ClassVar[int]
        X_FIELD_NUMBER: ClassVar[int]
        Y_FIELD_NUMBER: ClassVar[int]
        advance: float
        ascent: int
        character: int
        descent: int
        glyph_data_offset: int
        glyph_data_size: int
        left_bearing: float
        width: int
        x: int
        y: int
        def __init__(self, character: Optional[int] = ..., width: Optional[int] = ..., advance: Optional[float] = ..., left_bearing: Optional[float] = ..., ascent: Optional[int] = ..., descent: Optional[int] = ..., x: Optional[int] = ..., y: Optional[int] = ..., glyph_data_offset: Optional[int] = ..., glyph_data_size: Optional[int] = ...) -> None: ...
    CACHE_CELL_HEIGHT_FIELD_NUMBER: ClassVar[int]
    CACHE_CELL_MAX_ASCENT_FIELD_NUMBER: ClassVar[int]
    CACHE_CELL_WIDTH_FIELD_NUMBER: ClassVar[int]
    CACHE_HEIGHT_FIELD_NUMBER: ClassVar[int]
    CACHE_WIDTH_FIELD_NUMBER: ClassVar[int]
    GLYPHS_FIELD_NUMBER: ClassVar[int]
    GLYPH_CHANNELS_FIELD_NUMBER: ClassVar[int]
    GLYPH_DATA_FIELD_NUMBER: ClassVar[int]
    GLYPH_PADDING_FIELD_NUMBER: ClassVar[int]
    IMAGE_FORMAT_FIELD_NUMBER: ClassVar[int]
    IS_MONOSPACED_FIELD_NUMBER: ClassVar[int]
    MAX_ASCENT_FIELD_NUMBER: ClassVar[int]
    MAX_DESCENT_FIELD_NUMBER: ClassVar[int]
    PADDING_FIELD_NUMBER: ClassVar[int]
    SDF_OFFSET_FIELD_NUMBER: ClassVar[int]
    SDF_OUTLINE_FIELD_NUMBER: ClassVar[int]
    SDF_SHADOW_FIELD_NUMBER: ClassVar[int]
    SDF_SPREAD_FIELD_NUMBER: ClassVar[int]
    cache_cell_height: int
    cache_cell_max_ascent: int
    cache_cell_width: int
    cache_height: int
    cache_width: int
    glyph_channels: int
    glyph_data: bytes
    glyph_padding: int
    glyphs: _containers.RepeatedCompositeFieldContainer[GlyphBank.Glyph]
    image_format: FontTextureFormat
    is_monospaced: bool
    max_ascent: float
    max_descent: float
    padding: int
    sdf_offset: float
    sdf_outline: float
    sdf_shadow: float
    sdf_spread: float
    def __init__(self, glyphs: Optional[Iterable[Union[GlyphBank.Glyph, Mapping]]] = ..., glyph_padding: Optional[int] = ..., glyph_channels: Optional[int] = ..., glyph_data: Optional[bytes] = ..., max_ascent: Optional[float] = ..., max_descent: Optional[float] = ..., image_format: Optional[Union[FontTextureFormat, str]] = ..., sdf_spread: Optional[float] = ..., sdf_offset: Optional[float] = ..., sdf_outline: Optional[float] = ..., sdf_shadow: Optional[float] = ..., cache_width: Optional[int] = ..., cache_height: Optional[int] = ..., cache_cell_width: Optional[int] = ..., cache_cell_height: Optional[int] = ..., cache_cell_max_ascent: Optional[int] = ..., padding: Optional[int] = ..., is_monospaced: bool = ...) -> None: ...

class FontTextureFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class FontRenderMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
