from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor

class LayoutChanged(_message.Message):
    __slots__ = ["id", "previous_id"]
    ID_FIELD_NUMBER: ClassVar[int]
    PREVIOUS_ID_FIELD_NUMBER: ClassVar[int]
    id: int
    previous_id: int
    def __init__(self, id: Optional[int] = ..., previous_id: Optional[int] = ...) -> None: ...

class NodeDesc(_message.Message):
    __slots__ = ["adjust_mode", "alpha", "blend_mode", "clipping_inverted", "clipping_mode", "clipping_visible", "color", "custom_type", "enabled", "font", "id", "inherit_alpha", "innerRadius", "layer", "line_break", "material", "outerBounds", "outline", "outline_alpha", "overridden_fields", "parent", "particlefx", "perimeterVertices", "pieFillAngle", "pivot", "position", "rotation", "scale", "shadow", "shadow_alpha", "size", "size_mode", "slice9", "spine_default_animation", "spine_node_child", "spine_scene", "spine_skin", "template", "template_node_child", "text", "text_leading", "text_tracking", "texture", "type", "visible", "xanchor", "yanchor"]
    class AdjustMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class BlendMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class ClippingMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class PieBounds(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Pivot(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class SizeMode(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class Type(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class XAnchor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class YAnchor(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    ADJUST_MODE_FIELD_NUMBER: ClassVar[int]
    ADJUST_MODE_FIT: NodeDesc.AdjustMode
    ADJUST_MODE_STRETCH: NodeDesc.AdjustMode
    ADJUST_MODE_ZOOM: NodeDesc.AdjustMode
    ALPHA_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_ADD: NodeDesc.BlendMode
    BLEND_MODE_ADD_ALPHA: NodeDesc.BlendMode
    BLEND_MODE_ALPHA: NodeDesc.BlendMode
    BLEND_MODE_FIELD_NUMBER: ClassVar[int]
    BLEND_MODE_MULT: NodeDesc.BlendMode
    BLEND_MODE_SCREEN: NodeDesc.BlendMode
    CLIPPING_INVERTED_FIELD_NUMBER: ClassVar[int]
    CLIPPING_MODE_FIELD_NUMBER: ClassVar[int]
    CLIPPING_MODE_NONE: NodeDesc.ClippingMode
    CLIPPING_MODE_STENCIL: NodeDesc.ClippingMode
    CLIPPING_VISIBLE_FIELD_NUMBER: ClassVar[int]
    COLOR_FIELD_NUMBER: ClassVar[int]
    CUSTOM_TYPE_FIELD_NUMBER: ClassVar[int]
    ENABLED_FIELD_NUMBER: ClassVar[int]
    FONT_FIELD_NUMBER: ClassVar[int]
    ID_FIELD_NUMBER: ClassVar[int]
    INHERIT_ALPHA_FIELD_NUMBER: ClassVar[int]
    INNERRADIUS_FIELD_NUMBER: ClassVar[int]
    LAYER_FIELD_NUMBER: ClassVar[int]
    LINE_BREAK_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    OUTERBOUNDS_FIELD_NUMBER: ClassVar[int]
    OUTLINE_ALPHA_FIELD_NUMBER: ClassVar[int]
    OUTLINE_FIELD_NUMBER: ClassVar[int]
    OVERRIDDEN_FIELDS_FIELD_NUMBER: ClassVar[int]
    PARENT_FIELD_NUMBER: ClassVar[int]
    PARTICLEFX_FIELD_NUMBER: ClassVar[int]
    PERIMETERVERTICES_FIELD_NUMBER: ClassVar[int]
    PIEBOUNDS_ELLIPSE: NodeDesc.PieBounds
    PIEBOUNDS_RECTANGLE: NodeDesc.PieBounds
    PIEFILLANGLE_FIELD_NUMBER: ClassVar[int]
    PIVOT_CENTER: NodeDesc.Pivot
    PIVOT_E: NodeDesc.Pivot
    PIVOT_FIELD_NUMBER: ClassVar[int]
    PIVOT_N: NodeDesc.Pivot
    PIVOT_NE: NodeDesc.Pivot
    PIVOT_NW: NodeDesc.Pivot
    PIVOT_S: NodeDesc.Pivot
    PIVOT_SE: NodeDesc.Pivot
    PIVOT_SW: NodeDesc.Pivot
    PIVOT_W: NodeDesc.Pivot
    POSITION_FIELD_NUMBER: ClassVar[int]
    ROTATION_FIELD_NUMBER: ClassVar[int]
    SCALE_FIELD_NUMBER: ClassVar[int]
    SHADOW_ALPHA_FIELD_NUMBER: ClassVar[int]
    SHADOW_FIELD_NUMBER: ClassVar[int]
    SIZE_FIELD_NUMBER: ClassVar[int]
    SIZE_MODE_AUTO: NodeDesc.SizeMode
    SIZE_MODE_FIELD_NUMBER: ClassVar[int]
    SIZE_MODE_MANUAL: NodeDesc.SizeMode
    SLICE9_FIELD_NUMBER: ClassVar[int]
    SPINE_DEFAULT_ANIMATION_FIELD_NUMBER: ClassVar[int]
    SPINE_NODE_CHILD_FIELD_NUMBER: ClassVar[int]
    SPINE_SCENE_FIELD_NUMBER: ClassVar[int]
    SPINE_SKIN_FIELD_NUMBER: ClassVar[int]
    TEMPLATE_FIELD_NUMBER: ClassVar[int]
    TEMPLATE_NODE_CHILD_FIELD_NUMBER: ClassVar[int]
    TEXTURE_FIELD_NUMBER: ClassVar[int]
    TEXT_FIELD_NUMBER: ClassVar[int]
    TEXT_LEADING_FIELD_NUMBER: ClassVar[int]
    TEXT_TRACKING_FIELD_NUMBER: ClassVar[int]
    TYPE_BOX: NodeDesc.Type
    TYPE_CUSTOM: NodeDesc.Type
    TYPE_FIELD_NUMBER: ClassVar[int]
    TYPE_PARTICLEFX: NodeDesc.Type
    TYPE_PIE: NodeDesc.Type
    TYPE_SPINE: NodeDesc.Type
    TYPE_TEMPLATE: NodeDesc.Type
    TYPE_TEXT: NodeDesc.Type
    VISIBLE_FIELD_NUMBER: ClassVar[int]
    XANCHOR_FIELD_NUMBER: ClassVar[int]
    XANCHOR_LEFT: NodeDesc.XAnchor
    XANCHOR_NONE: NodeDesc.XAnchor
    XANCHOR_RIGHT: NodeDesc.XAnchor
    YANCHOR_BOTTOM: NodeDesc.YAnchor
    YANCHOR_FIELD_NUMBER: ClassVar[int]
    YANCHOR_NONE: NodeDesc.YAnchor
    YANCHOR_TOP: NodeDesc.YAnchor
    adjust_mode: NodeDesc.AdjustMode
    alpha: float
    blend_mode: NodeDesc.BlendMode
    clipping_inverted: bool
    clipping_mode: NodeDesc.ClippingMode
    clipping_visible: bool
    color: _ddf_math_pb2.Vector4One
    custom_type: int
    enabled: bool
    font: str
    id: str
    inherit_alpha: bool
    innerRadius: float
    layer: str
    line_break: bool
    material: str
    outerBounds: NodeDesc.PieBounds
    outline: _ddf_math_pb2.Vector4WOne
    outline_alpha: float
    overridden_fields: _containers.RepeatedScalarFieldContainer[int]
    parent: str
    particlefx: str
    perimeterVertices: int
    pieFillAngle: float
    pivot: NodeDesc.Pivot
    position: _ddf_math_pb2.Vector4
    rotation: _ddf_math_pb2.Vector4
    scale: _ddf_math_pb2.Vector4One
    shadow: _ddf_math_pb2.Vector4WOne
    shadow_alpha: float
    size: _ddf_math_pb2.Vector4
    size_mode: NodeDesc.SizeMode
    slice9: _ddf_math_pb2.Vector4
    spine_default_animation: str
    spine_node_child: bool
    spine_scene: str
    spine_skin: str
    template: str
    template_node_child: bool
    text: str
    text_leading: float
    text_tracking: float
    texture: str
    type: NodeDesc.Type
    visible: bool
    xanchor: NodeDesc.XAnchor
    yanchor: NodeDesc.YAnchor
    def __init__(self, position: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., rotation: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., scale: Optional[Union[_ddf_math_pb2.Vector4One, Mapping]] = ..., size: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., color: Optional[Union[_ddf_math_pb2.Vector4One, Mapping]] = ..., type: Optional[Union[NodeDesc.Type, str]] = ..., blend_mode: Optional[Union[NodeDesc.BlendMode, str]] = ..., text: Optional[str] = ..., texture: Optional[str] = ..., font: Optional[str] = ..., id: Optional[str] = ..., xanchor: Optional[Union[NodeDesc.XAnchor, str]] = ..., yanchor: Optional[Union[NodeDesc.YAnchor, str]] = ..., pivot: Optional[Union[NodeDesc.Pivot, str]] = ..., outline: Optional[Union[_ddf_math_pb2.Vector4WOne, Mapping]] = ..., shadow: Optional[Union[_ddf_math_pb2.Vector4WOne, Mapping]] = ..., adjust_mode: Optional[Union[NodeDesc.AdjustMode, str]] = ..., line_break: bool = ..., parent: Optional[str] = ..., layer: Optional[str] = ..., inherit_alpha: bool = ..., slice9: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., outerBounds: Optional[Union[NodeDesc.PieBounds, str]] = ..., innerRadius: Optional[float] = ..., perimeterVertices: Optional[int] = ..., pieFillAngle: Optional[float] = ..., clipping_mode: Optional[Union[NodeDesc.ClippingMode, str]] = ..., clipping_visible: bool = ..., clipping_inverted: bool = ..., alpha: Optional[float] = ..., outline_alpha: Optional[float] = ..., shadow_alpha: Optional[float] = ..., overridden_fields: Optional[Iterable[int]] = ..., template: Optional[str] = ..., template_node_child: bool = ..., text_leading: Optional[float] = ..., text_tracking: Optional[float] = ..., size_mode: Optional[Union[NodeDesc.SizeMode, str]] = ..., spine_scene: Optional[str] = ..., spine_default_animation: Optional[str] = ..., spine_skin: Optional[str] = ..., spine_node_child: bool = ..., particlefx: Optional[str] = ..., custom_type: Optional[int] = ..., enabled: bool = ..., visible: bool = ..., material: Optional[str] = ...) -> None: ...

class SceneDesc(_message.Message):
    __slots__ = ["adjust_reference", "background_color", "fonts", "layers", "layouts", "material", "materials", "max_dynamic_textures", "max_nodes", "nodes", "particlefxs", "resources", "script", "spine_scenes", "textures"]
    class AdjustReference(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = []
    class FontDesc(_message.Message):
        __slots__ = ["font", "name"]
        FONT_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        font: str
        name: str
        def __init__(self, name: Optional[str] = ..., font: Optional[str] = ...) -> None: ...
    class LayerDesc(_message.Message):
        __slots__ = ["name"]
        NAME_FIELD_NUMBER: ClassVar[int]
        name: str
        def __init__(self, name: Optional[str] = ...) -> None: ...
    class LayoutDesc(_message.Message):
        __slots__ = ["name", "nodes"]
        NAME_FIELD_NUMBER: ClassVar[int]
        NODES_FIELD_NUMBER: ClassVar[int]
        name: str
        nodes: _containers.RepeatedCompositeFieldContainer[NodeDesc]
        def __init__(self, name: Optional[str] = ..., nodes: Optional[Iterable[Union[NodeDesc, Mapping]]] = ...) -> None: ...
    class MaterialDesc(_message.Message):
        __slots__ = ["material", "name"]
        MATERIAL_FIELD_NUMBER: ClassVar[int]
        NAME_FIELD_NUMBER: ClassVar[int]
        material: str
        name: str
        def __init__(self, name: Optional[str] = ..., material: Optional[str] = ...) -> None: ...
    class ParticleFXDesc(_message.Message):
        __slots__ = ["name", "particlefx"]
        NAME_FIELD_NUMBER: ClassVar[int]
        PARTICLEFX_FIELD_NUMBER: ClassVar[int]
        name: str
        particlefx: str
        def __init__(self, name: Optional[str] = ..., particlefx: Optional[str] = ...) -> None: ...
    class ResourceDesc(_message.Message):
        __slots__ = ["name", "path"]
        NAME_FIELD_NUMBER: ClassVar[int]
        PATH_FIELD_NUMBER: ClassVar[int]
        name: str
        path: str
        def __init__(self, name: Optional[str] = ..., path: Optional[str] = ...) -> None: ...
    class SpineSceneDesc(_message.Message):
        __slots__ = ["name", "spine_scene"]
        NAME_FIELD_NUMBER: ClassVar[int]
        SPINE_SCENE_FIELD_NUMBER: ClassVar[int]
        name: str
        spine_scene: str
        def __init__(self, name: Optional[str] = ..., spine_scene: Optional[str] = ...) -> None: ...
    class TextureDesc(_message.Message):
        __slots__ = ["name", "texture"]
        NAME_FIELD_NUMBER: ClassVar[int]
        TEXTURE_FIELD_NUMBER: ClassVar[int]
        name: str
        texture: str
        def __init__(self, name: Optional[str] = ..., texture: Optional[str] = ...) -> None: ...
    ADJUST_REFERENCE_DISABLED: SceneDesc.AdjustReference
    ADJUST_REFERENCE_FIELD_NUMBER: ClassVar[int]
    ADJUST_REFERENCE_LEGACY: SceneDesc.AdjustReference
    ADJUST_REFERENCE_PARENT: SceneDesc.AdjustReference
    BACKGROUND_COLOR_FIELD_NUMBER: ClassVar[int]
    FONTS_FIELD_NUMBER: ClassVar[int]
    LAYERS_FIELD_NUMBER: ClassVar[int]
    LAYOUTS_FIELD_NUMBER: ClassVar[int]
    MATERIALS_FIELD_NUMBER: ClassVar[int]
    MATERIAL_FIELD_NUMBER: ClassVar[int]
    MAX_DYNAMIC_TEXTURES_FIELD_NUMBER: ClassVar[int]
    MAX_NODES_FIELD_NUMBER: ClassVar[int]
    NODES_FIELD_NUMBER: ClassVar[int]
    PARTICLEFXS_FIELD_NUMBER: ClassVar[int]
    RESOURCES_FIELD_NUMBER: ClassVar[int]
    SCRIPT_FIELD_NUMBER: ClassVar[int]
    SPINE_SCENES_FIELD_NUMBER: ClassVar[int]
    TEXTURES_FIELD_NUMBER: ClassVar[int]
    adjust_reference: SceneDesc.AdjustReference
    background_color: _ddf_math_pb2.Vector4
    fonts: _containers.RepeatedCompositeFieldContainer[SceneDesc.FontDesc]
    layers: _containers.RepeatedCompositeFieldContainer[SceneDesc.LayerDesc]
    layouts: _containers.RepeatedCompositeFieldContainer[SceneDesc.LayoutDesc]
    material: str
    materials: _containers.RepeatedCompositeFieldContainer[SceneDesc.MaterialDesc]
    max_dynamic_textures: int
    max_nodes: int
    nodes: _containers.RepeatedCompositeFieldContainer[NodeDesc]
    particlefxs: _containers.RepeatedCompositeFieldContainer[SceneDesc.ParticleFXDesc]
    resources: _containers.RepeatedCompositeFieldContainer[SceneDesc.ResourceDesc]
    script: str
    spine_scenes: _containers.RepeatedCompositeFieldContainer[SceneDesc.SpineSceneDesc]
    textures: _containers.RepeatedCompositeFieldContainer[SceneDesc.TextureDesc]
    def __init__(self, script: Optional[str] = ..., fonts: Optional[Iterable[Union[SceneDesc.FontDesc, Mapping]]] = ..., textures: Optional[Iterable[Union[SceneDesc.TextureDesc, Mapping]]] = ..., background_color: Optional[Union[_ddf_math_pb2.Vector4, Mapping]] = ..., nodes: Optional[Iterable[Union[NodeDesc, Mapping]]] = ..., layers: Optional[Iterable[Union[SceneDesc.LayerDesc, Mapping]]] = ..., material: Optional[str] = ..., layouts: Optional[Iterable[Union[SceneDesc.LayoutDesc, Mapping]]] = ..., adjust_reference: Optional[Union[SceneDesc.AdjustReference, str]] = ..., max_nodes: Optional[int] = ..., spine_scenes: Optional[Iterable[Union[SceneDesc.SpineSceneDesc, Mapping]]] = ..., particlefxs: Optional[Iterable[Union[SceneDesc.ParticleFXDesc, Mapping]]] = ..., resources: Optional[Iterable[Union[SceneDesc.ResourceDesc, Mapping]]] = ..., materials: Optional[Iterable[Union[SceneDesc.MaterialDesc, Mapping]]] = ..., max_dynamic_textures: Optional[int] = ...) -> None: ...
