from ddf import ddf_extensions_pb2 as _ddf_extensions_pb2
from ddf import ddf_math_pb2 as _ddf_math_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar, Iterable, Mapping, Optional, Union

DESCRIPTOR: _descriptor.FileDescriptor
GAMEPAD_BACK: Gamepad
GAMEPAD_CONNECTED: Gamepad
GAMEPAD_DISCONNECTED: Gamepad
GAMEPAD_GUIDE: Gamepad
GAMEPAD_LPAD_DOWN: Gamepad
GAMEPAD_LPAD_LEFT: Gamepad
GAMEPAD_LPAD_RIGHT: Gamepad
GAMEPAD_LPAD_UP: Gamepad
GAMEPAD_LSHOULDER: Gamepad
GAMEPAD_LSTICK_CLICK: Gamepad
GAMEPAD_LSTICK_DOWN: Gamepad
GAMEPAD_LSTICK_LEFT: Gamepad
GAMEPAD_LSTICK_RIGHT: Gamepad
GAMEPAD_LSTICK_UP: Gamepad
GAMEPAD_LTRIGGER: Gamepad
GAMEPAD_MODIFIER_CLAMP: GamepadModifier
GAMEPAD_MODIFIER_NEGATE: GamepadModifier
GAMEPAD_MODIFIER_SCALE: GamepadModifier
GAMEPAD_RAW: Gamepad
GAMEPAD_RPAD_DOWN: Gamepad
GAMEPAD_RPAD_LEFT: Gamepad
GAMEPAD_RPAD_RIGHT: Gamepad
GAMEPAD_RPAD_UP: Gamepad
GAMEPAD_RSHOULDER: Gamepad
GAMEPAD_RSTICK_CLICK: Gamepad
GAMEPAD_RSTICK_DOWN: Gamepad
GAMEPAD_RSTICK_LEFT: Gamepad
GAMEPAD_RSTICK_RIGHT: Gamepad
GAMEPAD_RSTICK_UP: Gamepad
GAMEPAD_RTRIGGER: Gamepad
GAMEPAD_START: Gamepad
GAMEPAD_TYPE_AXIS: GamepadType
GAMEPAD_TYPE_BUTTON: GamepadType
GAMEPAD_TYPE_HAT: GamepadType
KEY_0: Key
KEY_1: Key
KEY_2: Key
KEY_3: Key
KEY_4: Key
KEY_5: Key
KEY_6: Key
KEY_7: Key
KEY_8: Key
KEY_9: Key
KEY_A: Key
KEY_AMPERSAND: Key
KEY_ASTERISK: Key
KEY_AT: Key
KEY_B: Key
KEY_BACK: Key
KEY_BACKQUOTE: Key
KEY_BACKSLASH: Key
KEY_BACKSPACE: Key
KEY_C: Key
KEY_CAPS_LOCK: Key
KEY_CARET: Key
KEY_COLON: Key
KEY_COMMA: Key
KEY_D: Key
KEY_DEL: Key
KEY_DOLLAR: Key
KEY_DOWN: Key
KEY_E: Key
KEY_END: Key
KEY_ENTER: Key
KEY_EQUALS: Key
KEY_ESC: Key
KEY_EXCLAIM: Key
KEY_F: Key
KEY_F1: Key
KEY_F10: Key
KEY_F11: Key
KEY_F12: Key
KEY_F2: Key
KEY_F3: Key
KEY_F4: Key
KEY_F5: Key
KEY_F6: Key
KEY_F7: Key
KEY_F8: Key
KEY_F9: Key
KEY_G: Key
KEY_GREATER: Key
KEY_H: Key
KEY_HASH: Key
KEY_HOME: Key
KEY_I: Key
KEY_INSERT: Key
KEY_J: Key
KEY_K: Key
KEY_KP_0: Key
KEY_KP_1: Key
KEY_KP_2: Key
KEY_KP_3: Key
KEY_KP_4: Key
KEY_KP_5: Key
KEY_KP_6: Key
KEY_KP_7: Key
KEY_KP_8: Key
KEY_KP_9: Key
KEY_KP_ADD: Key
KEY_KP_DECIMAL: Key
KEY_KP_DIVIDE: Key
KEY_KP_ENTER: Key
KEY_KP_EQUAL: Key
KEY_KP_MULTIPLY: Key
KEY_KP_NUM_LOCK: Key
KEY_KP_SUBTRACT: Key
KEY_L: Key
KEY_LALT: Key
KEY_LBRACE: Key
KEY_LBRACKET: Key
KEY_LCTRL: Key
KEY_LEFT: Key
KEY_LESS: Key
KEY_LPAREN: Key
KEY_LSHIFT: Key
KEY_LSUPER: Key
KEY_M: Key
KEY_MENU: Key
KEY_MINUS: Key
KEY_N: Key
KEY_O: Key
KEY_P: Key
KEY_PAGEDOWN: Key
KEY_PAGEUP: Key
KEY_PAUSE: Key
KEY_PERIOD: Key
KEY_PIPE: Key
KEY_PLUS: Key
KEY_Q: Key
KEY_QUESTION: Key
KEY_QUOTE: Key
KEY_QUOTEDBL: Key
KEY_R: Key
KEY_RALT: Key
KEY_RBRACE: Key
KEY_RBRACKET: Key
KEY_RCTRL: Key
KEY_RIGHT: Key
KEY_RPAREN: Key
KEY_RSHIFT: Key
KEY_RSUPER: Key
KEY_S: Key
KEY_SCROLL_LOCK: Key
KEY_SEMICOLON: Key
KEY_SLASH: Key
KEY_SPACE: Key
KEY_T: Key
KEY_TAB: Key
KEY_TILDE: Key
KEY_U: Key
KEY_UNDERSCORE: Key
KEY_UP: Key
KEY_V: Key
KEY_W: Key
KEY_X: Key
KEY_Y: Key
KEY_Z: Key
MARKED_TEXT: Text
MAX_GAMEPAD_COUNT: Gamepad
MAX_GAMEPAD_MODIFIER_COUNT: GamepadModifier
MAX_KEY_COUNT: Key
MAX_MOUSE_COUNT: Mouse
MAX_TEXT_COUNT: Text
MAX_TOUCH_COUNT: Touch
MOUSE_BUTTON_1: Mouse
MOUSE_BUTTON_2: Mouse
MOUSE_BUTTON_3: Mouse
MOUSE_BUTTON_4: Mouse
MOUSE_BUTTON_5: Mouse
MOUSE_BUTTON_6: Mouse
MOUSE_BUTTON_7: Mouse
MOUSE_BUTTON_8: Mouse
MOUSE_BUTTON_LEFT: Mouse
MOUSE_BUTTON_MIDDLE: Mouse
MOUSE_BUTTON_RIGHT: Mouse
MOUSE_WHEEL_DOWN: Mouse
MOUSE_WHEEL_UP: Mouse
TEXT: Text
TOUCH_MULTI: Touch

class GamepadMap(_message.Message):
    __slots__ = ["dead_zone", "device", "map", "platform"]
    DEAD_ZONE_FIELD_NUMBER: ClassVar[int]
    DEVICE_FIELD_NUMBER: ClassVar[int]
    MAP_FIELD_NUMBER: ClassVar[int]
    PLATFORM_FIELD_NUMBER: ClassVar[int]
    dead_zone: float
    device: str
    map: _containers.RepeatedCompositeFieldContainer[GamepadMapEntry]
    platform: str
    def __init__(self, device: Optional[str] = ..., platform: Optional[str] = ..., dead_zone: Optional[float] = ..., map: Optional[Iterable[Union[GamepadMapEntry, Mapping]]] = ...) -> None: ...

class GamepadMapEntry(_message.Message):
    __slots__ = ["hat_mask", "index", "input", "mod", "type"]
    HAT_MASK_FIELD_NUMBER: ClassVar[int]
    INDEX_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    MOD_FIELD_NUMBER: ClassVar[int]
    TYPE_FIELD_NUMBER: ClassVar[int]
    hat_mask: int
    index: int
    input: Gamepad
    mod: _containers.RepeatedCompositeFieldContainer[GamepadModifier_t]
    type: GamepadType
    def __init__(self, input: Optional[Union[Gamepad, str]] = ..., type: Optional[Union[GamepadType, str]] = ..., index: Optional[int] = ..., mod: Optional[Iterable[Union[GamepadModifier_t, Mapping]]] = ..., hat_mask: Optional[int] = ...) -> None: ...

class GamepadMaps(_message.Message):
    __slots__ = ["driver"]
    DRIVER_FIELD_NUMBER: ClassVar[int]
    driver: _containers.RepeatedCompositeFieldContainer[GamepadMap]
    def __init__(self, driver: Optional[Iterable[Union[GamepadMap, Mapping]]] = ...) -> None: ...

class GamepadModifier_t(_message.Message):
    __slots__ = ["mod"]
    MOD_FIELD_NUMBER: ClassVar[int]
    mod: GamepadModifier
    def __init__(self, mod: Optional[Union[GamepadModifier, str]] = ...) -> None: ...

class GamepadTrigger(_message.Message):
    __slots__ = ["action", "input"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    action: str
    input: Gamepad
    def __init__(self, input: Optional[Union[Gamepad, str]] = ..., action: Optional[str] = ...) -> None: ...

class InputBinding(_message.Message):
    __slots__ = ["gamepad_trigger", "key_trigger", "mouse_trigger", "text_trigger", "touch_trigger"]
    GAMEPAD_TRIGGER_FIELD_NUMBER: ClassVar[int]
    KEY_TRIGGER_FIELD_NUMBER: ClassVar[int]
    MOUSE_TRIGGER_FIELD_NUMBER: ClassVar[int]
    TEXT_TRIGGER_FIELD_NUMBER: ClassVar[int]
    TOUCH_TRIGGER_FIELD_NUMBER: ClassVar[int]
    gamepad_trigger: _containers.RepeatedCompositeFieldContainer[GamepadTrigger]
    key_trigger: _containers.RepeatedCompositeFieldContainer[KeyTrigger]
    mouse_trigger: _containers.RepeatedCompositeFieldContainer[MouseTrigger]
    text_trigger: _containers.RepeatedCompositeFieldContainer[TextTrigger]
    touch_trigger: _containers.RepeatedCompositeFieldContainer[TouchTrigger]
    def __init__(self, key_trigger: Optional[Iterable[Union[KeyTrigger, Mapping]]] = ..., mouse_trigger: Optional[Iterable[Union[MouseTrigger, Mapping]]] = ..., gamepad_trigger: Optional[Iterable[Union[GamepadTrigger, Mapping]]] = ..., touch_trigger: Optional[Iterable[Union[TouchTrigger, Mapping]]] = ..., text_trigger: Optional[Iterable[Union[TextTrigger, Mapping]]] = ...) -> None: ...

class KeyTrigger(_message.Message):
    __slots__ = ["action", "input"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    action: str
    input: Key
    def __init__(self, input: Optional[Union[Key, str]] = ..., action: Optional[str] = ...) -> None: ...

class MouseTrigger(_message.Message):
    __slots__ = ["action", "input"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    action: str
    input: Mouse
    def __init__(self, input: Optional[Union[Mouse, str]] = ..., action: Optional[str] = ...) -> None: ...

class TextTrigger(_message.Message):
    __slots__ = ["action", "input"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    action: str
    input: Text
    def __init__(self, input: Optional[Union[Text, str]] = ..., action: Optional[str] = ...) -> None: ...

class TouchTrigger(_message.Message):
    __slots__ = ["action", "input"]
    ACTION_FIELD_NUMBER: ClassVar[int]
    INPUT_FIELD_NUMBER: ClassVar[int]
    action: str
    input: Touch
    def __init__(self, input: Optional[Union[Touch, str]] = ..., action: Optional[str] = ...) -> None: ...

class Key(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Mouse(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Gamepad(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class GamepadType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class GamepadModifier(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Touch(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []

class Text(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
