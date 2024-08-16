from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

COORDINATE_SPACE_LOCAL: CoordinateSpace
COORDINATE_SPACE_WORLD: CoordinateSpace
DEPTH_STENCIL_FORMAT_D16U_S8U: DepthStencilFormat
DEPTH_STENCIL_FORMAT_D24U_S8U: DepthStencilFormat
DEPTH_STENCIL_FORMAT_D32F: DepthStencilFormat
DEPTH_STENCIL_FORMAT_D32F_S8U: DepthStencilFormat
DEPTH_STENCIL_FORMAT_S8U: DepthStencilFormat
DESCRIPTOR: _descriptor.FileDescriptor
TEXTURE_USAGE_FLAG_COLOR: TextureUsageFlag
TEXTURE_USAGE_FLAG_INPUT: TextureUsageFlag
TEXTURE_USAGE_FLAG_MEMORYLESS: TextureUsageFlag
TEXTURE_USAGE_FLAG_SAMPLE: TextureUsageFlag
TEXTURE_USAGE_FLAG_STORAGE: TextureUsageFlag

class Cubemap(_message.Message):
    __slots__ = ["back", "bottom", "front", "left", "right", "top"]
    BACK_FIELD_NUMBER: ClassVar[int]
    BOTTOM_FIELD_NUMBER: ClassVar[int]
    FRONT_FIELD_NUMBER: ClassVar[int]
    LEFT_FIELD_NUMBER: ClassVar[int]
    RIGHT_FIELD_NUMBER: ClassVar[int]
    TOP_FIELD_NUMBER: ClassVar[int]
    back: str
    bottom: str
    front: str
    left: str
    right: str
    top: str
    def __init__(self, right: Optional[str] = ..., left: Optional[str] = ..., top: Optional[str] = ..., bottom: Optional[str] = ..., front: Optional[str] = ..., back: Optional[str] = ...) -> None: ...

class PathSettings(_message.Message):
    __slots__ = ["path", "profile"]
    PATH_FIELD_NUMBER: ClassVar[int]
    PROFILE_FIELD_NUMBER: ClassVar[int]
    path: str
    profile: str
    def __init__(self, path: Optional[str] = ..., profile: Optional[str] = ...) -> None: ...

class PlatformProfile(_message.Message):
    __slots__ = ["formats", "max_texture_size", "mipmaps", "os", "premultiply_alpha"]
    class OS(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    FORMATS_FIELD_NUMBER: ClassVar[int]
    MAX_TEXTURE_SIZE_FIELD_NUMBER: ClassVar[int]
    MIPMAPS_FIELD_NUMBER: ClassVar[int]
    OS_FIELD_NUMBER: ClassVar[int]
    OS_ID_ANDROID: PlatformProfile.OS
    OS_ID_GENERIC: PlatformProfile.OS
    OS_ID_IOS: PlatformProfile.OS
    OS_ID_LINUX: PlatformProfile.OS
    OS_ID_OSX: PlatformProfile.OS
    OS_ID_PS4: PlatformProfile.OS
    OS_ID_PS5: PlatformProfile.OS
    OS_ID_SWITCH: PlatformProfile.OS
    OS_ID_WEB: PlatformProfile.OS
    OS_ID_WINDOWS: PlatformProfile.OS
    PREMULTIPLY_ALPHA_FIELD_NUMBER: ClassVar[int]
    formats: _containers.RepeatedCompositeFieldContainer[TextureFormatAlternative]
    max_texture_size: int
    mipmaps: bool
    os: PlatformProfile.OS
    premultiply_alpha: bool
    def __init__(self, os: Optional[Union[PlatformProfile.OS, str]] = ..., formats: Optional[Iterable[Union[TextureFormatAlternative, Mapping]]] = ..., mipmaps: bool = ..., max_texture_size: Optional[int] = ..., premultiply_alpha: bool = ...) -> None: ...

class ShaderDesc(_message.Message):
    __slots__ = ["reflection", "shader_type", "shaders"]
    class Language(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ShaderDataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ShaderType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ResourceBinding(_message.Message):
        __slots__ = ["binding", "block_size", "name", "name_hash", "set", "type"]
        BINDING_FIELD_NUMBER: ClassVar[int]
        BLOCK_SIZE_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        NAME_HASH_FIELD_NUMBER: ClassVar[int]
        SET_FIELD_NUMBER: ClassVar[int]
        TYPE_FIELD_NUMBER: ClassVar[int]
        binding: int
        block_size: int
        name: str
        name_hash: int
        set: int
        type: ShaderDesc.ResourceType
        def __init__(self, name: Optional[str] = ..., name_hash: Optional[int] = ..., type: Optional[Union[ShaderDesc.ResourceType, Mapping]] = ..., set: Optional[int] = ..., binding: Optional[int] = ..., block_size: Optional[int] = ...) -> None: ...
    class ResourceMember(_message.Message):
        __slots__ = ["element_count", "name", "name_hash", "offset", "type"]
        ELEMENT_COUNT_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        NAME_HASH_FIELD_NUMBER: ClassVar[int]
        OFFSET_FIELD_NUMBER: ClassVar[int]
        TYPE_FIELD_NUMBER: ClassVar[int]
        element_count: int
        name: str
        name_hash: int
        offset: int
        type: ShaderDesc.ResourceType
        def __init__(self, name: Optional[str] = ..., name_hash: Optional[int] = ..., type: Optional[Union[ShaderDesc.ResourceType, Mapping]] = ..., element_count: Optional[int] = ..., offset: Optional[int] = ...) -> None: ...
    class ResourceType(_message.Message):
        __slots__ = ["shader_type", "type_index", "use_type_index"]
        SHADER_TYPE_FIELD_NUMBER: ClassVar[int]
        TYPE_INDEX_FIELD_NUMBER: ClassVar[int]
        USE_TYPE_INDEX_FIELD_NUMBER: ClassVar[int]
        shader_type: ShaderDesc.ShaderDataType
        type_index: int
        use_type_index: bool
        def __init__(self, shader_type: Optional[Union[ShaderDesc.ShaderDataType, str]] = ..., type_index: Optional[int] = ..., use_type_index: bool = ...) -> None: ...
    class ResourceTypeInfo(_message.Message):
        __slots__ = ["members", "name", "name_hash"]
        MEMBERS_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        NAME_HASH_FIELD_NUMBER: ClassVar[int]
        members: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceMember]
        name: str
        name_hash: int
        def __init__(self, name: Optional[str] = ..., name_hash: Optional[int] = ..., members: Optional[Iterable[Union[ShaderDesc.ResourceMember, Mapping]]] = ...) -> None: ...
    class Shader(_message.Message):
        __slots__ = ["language", "name", "source", "variant_texture_array"]
        LANGUAGE_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        SOURCE_FIELD_NUMBER: ClassVar[int]
        VARIANT_TEXTURE_ARRAY_FIELD_NUMBER: ClassVar[int]
        language: ShaderDesc.Language
        name: str
        source: bytes
        variant_texture_array: bool
        def __init__(self, language: Optional[Union[ShaderDesc.Language, str]] = ..., source: Optional[bytes] = ..., name: Optional[str] = ..., variant_texture_array: bool = ...) -> None: ...
    class ShaderReflection(_message.Message):
        __slots__ = ["inputs", "outputs", "storage_buffers", "textures", "types", "uniform_buffers"]
        INPUTS_FIELD_NUMBER: ClassVar[int]
        OUTPUTS_FIELD_NUMBER: ClassVar[int]
        STORAGE_BUFFERS_FIELD_NUMBER: ClassVar[int]
        TEXTURES_FIELD_NUMBER: ClassVar[int]
        TYPES_FIELD_NUMBER: ClassVar[int]
        UNIFORM_BUFFERS_FIELD_NUMBER: ClassVar[int]
        inputs: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceBinding]
        outputs: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceBinding]
        storage_buffers: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceBinding]
        textures: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceBinding]
        types: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceTypeInfo]
        uniform_buffers: _containers.RepeatedCompositeFieldContainer[ShaderDesc.ResourceBinding]
        def __init__(self, uniform_buffers: Optional[Iterable[Union[ShaderDesc.ResourceBinding, Mapping]]] = ..., storage_buffers: Optional[Iterable[Union[ShaderDesc.ResourceBinding, Mapping]]] = ..., textures: Optional[Iterable[Union[ShaderDesc.ResourceBinding, Mapping]]] = ..., inputs: Optional[Iterable[Union[ShaderDesc.ResourceBinding, Mapping]]] = ..., outputs: Optional[Iterable[Union[ShaderDesc.ResourceBinding, Mapping]]] = ..., types: Optional[Iterable[Union[ShaderDesc.ResourceTypeInfo, Mapping]]] = ...) -> None: ...
    LANGUAGE_GLES_SM100: ShaderDesc.Language
    LANGUAGE_GLES_SM300: ShaderDesc.Language
    LANGUAGE_GLSL_SM120: ShaderDesc.Language
    LANGUAGE_GLSL_SM140: ShaderDesc.Language
    LANGUAGE_GLSL_SM330: ShaderDesc.Language
    LANGUAGE_GLSL_SM430: ShaderDesc.Language
    LANGUAGE_PSSL: ShaderDesc.Language
    LANGUAGE_SPIRV: ShaderDesc.Language
    REFLECTION_FIELD_NUMBER: ClassVar[int]
    SHADERS_FIELD_NUMBER: ClassVar[int]
    SHADER_TYPE_COMPUTE: ShaderDesc.ShaderType
    SHADER_TYPE_FIELD_NUMBER: ClassVar[int]
    SHADER_TYPE_FLOAT: ShaderDesc.ShaderDataType
    SHADER_TYPE_FRAGMENT: ShaderDesc.ShaderType
    SHADER_TYPE_IMAGE2D: ShaderDesc.ShaderDataType
    SHADER_TYPE_INT: ShaderDesc.ShaderDataType
    SHADER_TYPE_MAT2: ShaderDesc.ShaderDataType
    SHADER_TYPE_MAT3: ShaderDesc.ShaderDataType
    SHADER_TYPE_MAT4: ShaderDesc.ShaderDataType
    SHADER_TYPE_RENDER_PASS_INPUT: ShaderDesc.ShaderDataType
    SHADER_TYPE_SAMPLER: ShaderDesc.ShaderDataType
    SHADER_TYPE_SAMPLER2D: ShaderDesc.ShaderDataType
    SHADER_TYPE_SAMPLER2D_ARRAY: ShaderDesc.ShaderDataType
    SHADER_TYPE_SAMPLER3D: ShaderDesc.ShaderDataType
    SHADER_TYPE_SAMPLER_CUBE: ShaderDesc.ShaderDataType
    SHADER_TYPE_STORAGE_BUFFER: ShaderDesc.ShaderDataType
    SHADER_TYPE_TEXTURE2D: ShaderDesc.ShaderDataType
    SHADER_TYPE_UIMAGE2D: ShaderDesc.ShaderDataType
    SHADER_TYPE_UINT: ShaderDesc.ShaderDataType
    SHADER_TYPE_UNIFORM_BUFFER: ShaderDesc.ShaderDataType
    SHADER_TYPE_UNKNOWN: ShaderDesc.ShaderDataType
    SHADER_TYPE_UTEXTURE2D: ShaderDesc.ShaderDataType
    SHADER_TYPE_UVEC2: ShaderDesc.ShaderDataType
    SHADER_TYPE_UVEC3: ShaderDesc.ShaderDataType
    SHADER_TYPE_UVEC4: ShaderDesc.ShaderDataType
    SHADER_TYPE_VEC2: ShaderDesc.ShaderDataType
    SHADER_TYPE_VEC3: ShaderDesc.ShaderDataType
    SHADER_TYPE_VEC4: ShaderDesc.ShaderDataType
    SHADER_TYPE_VERTEX: ShaderDesc.ShaderType
    reflection: ShaderDesc.ShaderReflection
    shader_type: ShaderDesc.ShaderType
    shaders: _containers.RepeatedCompositeFieldContainer[ShaderDesc.Shader]
    def __init__(self, shaders: Optional[Iterable[Union[ShaderDesc.Shader, Mapping]]] = ..., reflection: Optional[Union[ShaderDesc.ShaderReflection, Mapping]] = ..., shader_type: Optional[Union[ShaderDesc.ShaderType, str]] = ...) -> None: ...

class TextureFormatAlternative(_message.Message):
    __slots__ = ["compression_level", "compression_type", "format"]
    class CompressionLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    BEST: TextureFormatAlternative.CompressionLevel
    COMPRESSION_LEVEL_FIELD_NUMBER: ClassVar[int]
    COMPRESSION_TYPE_FIELD_NUMBER: ClassVar[int]
    FAST: TextureFormatAlternative.CompressionLevel
    FORMAT_FIELD_NUMBER: ClassVar[int]
    HIGH: TextureFormatAlternative.CompressionLevel
    NORMAL: TextureFormatAlternative.CompressionLevel
    compression_level: TextureFormatAlternative.CompressionLevel
    compression_type: TextureImage.CompressionType
    format: TextureImage.TextureFormat
    def __init__(self, format: Optional[Union[TextureImage.TextureFormat, str]] = ..., compression_level: Optional[Union[TextureFormatAlternative.CompressionLevel, str]] = ..., compression_type: Optional[Union[TextureImage.CompressionType, str]] = ...) -> None: ...

class TextureImage(_message.Message):
    __slots__ = ["alternatives", "count", "type", "usage_flags"]
    class CompressionFlags(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class CompressionType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class TextureFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Image(_message.Message):
        __slots__ = ["compression_flags", "compression_type", "data", "format", "height", "mip_map_offset", "mip_map_size", "mip_map_size_compressed", "original_height", "original_width", "width"]
        COMPRESSION_FLAGS_FIELD_NUMBER: ClassVar[int]
        COMPRESSION_TYPE_FIELD_NUMBER: ClassVar[int]
        DATA_FIELD_NUMBER: ClassVar[int]
        FORMAT_FIELD_NUMBER: ClassVar[int]
        HEIGHT_FIELD_NUMBER: ClassVar[int]
        MIP_MAP_OFFSET_FIELD_NUMBER: ClassVar[int]
        MIP_MAP_SIZE_COMPRESSED_FIELD_NUMBER: ClassVar[int]
        MIP_MAP_SIZE_FIELD_NUMBER: ClassVar[int]
        ORIGINAL_HEIGHT_FIELD_NUMBER: ClassVar[int]
        ORIGINAL_WIDTH_FIELD_NUMBER: ClassVar[int]
        WIDTH_FIELD_NUMBER: ClassVar[int]
        compression_flags: int
        compression_type: TextureImage.CompressionType
        data: bytes
        format: TextureImage.TextureFormat
        height: int
        mip_map_offset: _containers.RepeatedScalarFieldContainer[int]
        mip_map_size: _containers.RepeatedScalarFieldContainer[int]
        mip_map_size_compressed: _containers.RepeatedScalarFieldContainer[int]
        original_height: int
        original_width: int
        width: int
        def __init__(self, width: Optional[int] = ..., height: Optional[int] = ..., original_width: Optional[int] = ..., original_height: Optional[int] = ..., format: Optional[Union[TextureImage.TextureFormat, str]] = ..., mip_map_offset: Optional[Iterable[int]] = ..., mip_map_size: Optional[Iterable[int]] = ..., data: Optional[bytes] = ..., compression_type: Optional[Union[TextureImage.CompressionType, str]] = ..., compression_flags: Optional[int] = ..., mip_map_size_compressed: Optional[Iterable[int]] = ...) -> None: ...
    ALTERNATIVES_FIELD_NUMBER: ClassVar[int]
    COMPRESSION_FLAG_ALPHA_CLEAN: TextureImage.CompressionFlags
    COMPRESSION_TYPE_BASIS_ETC1S: TextureImage.CompressionType
    COMPRESSION_TYPE_BASIS_UASTC: TextureImage.CompressionType
    COMPRESSION_TYPE_DEFAULT: TextureImage.CompressionType
    COMPRESSION_TYPE_WEBP: TextureImage.CompressionType
    COMPRESSION_TYPE_WEBP_LOSSY: TextureImage.CompressionType
    COUNT_FIELD_NUMBER: ClassVar[int]
    TEXTURE_FORMAT_LUMINANCE: TextureImage.TextureFormat
    TEXTURE_FORMAT_LUMINANCE_ALPHA: TextureImage.TextureFormat
    TEXTURE_FORMAT_R16F: TextureImage.TextureFormat
    TEXTURE_FORMAT_R32F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RG16F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RG32F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB16F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB32F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA16F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA32F: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_16BPP: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_ASTC_4x4: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_BC3: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_BC7: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_ETC2: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_PVRTC_2BPPV1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGBA_PVRTC_4BPPV1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB_16BPP: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB_BC1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB_ETC1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB_PVRTC_2BPPV1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RGB_PVRTC_4BPPV1: TextureImage.TextureFormat
    TEXTURE_FORMAT_RG_BC5: TextureImage.TextureFormat
    TEXTURE_FORMAT_R_BC4: TextureImage.TextureFormat
    TYPE_2D: TextureImage.Type
    TYPE_2D_ARRAY: TextureImage.Type
    TYPE_2D_IMAGE: TextureImage.Type
    TYPE_CUBEMAP: TextureImage.Type
    TYPE_FIELD_NUMBER: ClassVar[int]
    USAGE_FLAGS_FIELD_NUMBER: ClassVar[int]
    alternatives: _containers.RepeatedCompositeFieldContainer[TextureImage.Image]
    count: int
    type: TextureImage.Type
    usage_flags: int
    def __init__(self, alternatives: Optional[Iterable[Union[TextureImage.Image, Mapping]]] = ..., type: Optional[Union[TextureImage.Type, str]] = ..., count: Optional[int] = ..., usage_flags: Optional[int] = ...) -> None: ...

class TextureProfile(_message.Message):
    __slots__ = ["name", "platforms"]
    NAME_FIELD_NUMBER: ClassVar[int]
    PLATFORMS_FIELD_NUMBER: ClassVar[int]
    name: str
    platforms: _containers.RepeatedCompositeFieldContainer[PlatformProfile]
    def __init__(self, name: Optional[str] = ..., platforms: Optional[Iterable[Union[PlatformProfile, Mapping]]] = ...) -> None: ...

class TextureProfiles(_message.Message):
    __slots__ = ["path_settings", "profiles"]
    PATH_SETTINGS_FIELD_NUMBER: ClassVar[int]
    PROFILES_FIELD_NUMBER: ClassVar[int]
    path_settings: _containers.RepeatedCompositeFieldContainer[PathSettings]
    profiles: _containers.RepeatedCompositeFieldContainer[TextureProfile]
    def __init__(self, path_settings: Optional[Iterable[Union[PathSettings, Mapping]]] = ..., profiles: Optional[Iterable[Union[TextureProfile, Mapping]]] = ...) -> None: ...

class VertexAttribute(_message.Message):
    __slots__ = ["binary_values", "coordinate_space", "data_type", "double_values", "element_count", "long_values", "name", "name_hash", "normalize", "semantic_type"]
    class DataType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SemanticType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class DoubleValues(_message.Message):
        __slots__ = ["v"]
        V_FIELD_NUMBER: ClassVar[int]
        v: _containers.RepeatedScalarFieldContainer[float]
        def __init__(self, v: Optional[Iterable[float]] = ...) -> None: ...
    class LongValues(_message.Message):
        __slots__ = ["v"]
        V_FIELD_NUMBER: ClassVar[int]
        v: _containers.RepeatedScalarFieldContainer[int]
        def __init__(self, v: Optional[Iterable[int]] = ...) -> None: ...
    BINARY_VALUES_FIELD_NUMBER: ClassVar[int]
    COORDINATE_SPACE_FIELD_NUMBER: ClassVar[int]
    DATA_TYPE_FIELD_NUMBER: ClassVar[int]
    DOUBLE_VALUES_FIELD_NUMBER: ClassVar[int]
    ELEMENT_COUNT_FIELD_NUMBER: ClassVar[int]
    LONG_VALUES_FIELD_NUMBER: ClassVar[int]
    NAME_FIELD_NUMBER: ClassVar[int]
    NAME_HASH_FIELD_NUMBER: ClassVar[int]
    NORMALIZE_FIELD_NUMBER: ClassVar[int]
    SEMANTIC_TYPE_COLOR: VertexAttribute.SemanticType
    SEMANTIC_TYPE_FIELD_NUMBER: ClassVar[int]
    SEMANTIC_TYPE_NONE: VertexAttribute.SemanticType
    SEMANTIC_TYPE_NORMAL: VertexAttribute.SemanticType
    SEMANTIC_TYPE_PAGE_INDEX: VertexAttribute.SemanticType
    SEMANTIC_TYPE_POSITION: VertexAttribute.SemanticType
    SEMANTIC_TYPE_TANGENT: VertexAttribute.SemanticType
    SEMANTIC_TYPE_TEXCOORD: VertexAttribute.SemanticType
    TYPE_BYTE: VertexAttribute.DataType
    TYPE_FLOAT: VertexAttribute.DataType
    TYPE_INT: VertexAttribute.DataType
    TYPE_SHORT: VertexAttribute.DataType
    TYPE_UNSIGNED_BYTE: VertexAttribute.DataType
    TYPE_UNSIGNED_INT: VertexAttribute.DataType
    TYPE_UNSIGNED_SHORT: VertexAttribute.DataType
    binary_values: bytes
    coordinate_space: CoordinateSpace
    data_type: VertexAttribute.DataType
    double_values: VertexAttribute.DoubleValues
    element_count: int
    long_values: VertexAttribute.LongValues
    name: str
    name_hash: int
    normalize: bool
    semantic_type: VertexAttribute.SemanticType
    def __init__(self, name: Optional[str] = ..., name_hash: Optional[int] = ..., semantic_type: Optional[Union[VertexAttribute.SemanticType, str]] = ..., element_count: Optional[int] = ..., normalize: bool = ..., data_type: Optional[Union[VertexAttribute.DataType, str]] = ..., coordinate_space: Optional[Union[CoordinateSpace, str]] = ..., long_values: Optional[Union[VertexAttribute.LongValues, Mapping]] = ..., double_values: Optional[Union[VertexAttribute.DoubleValues, Mapping]] = ..., binary_values: Optional[bytes] = ...) -> None: ...

class CoordinateSpace(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class DepthStencilFormat(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class TextureUsageFlag(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
