from enum import Enum


class apps(Enum):
    Desktop = 0
    Houdini = 1
    Maya = 2


class severityType(Enum):
    Message = 0
    ImportantMessage = 1
    Warning = 2
    Error = 3
    Fatal = 4


class messageTypes(Enum):
    check_for_update = 0
    disconnect = 1