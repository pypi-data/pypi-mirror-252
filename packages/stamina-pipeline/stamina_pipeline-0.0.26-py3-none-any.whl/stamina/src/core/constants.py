from enum import Enum
import os
import userpaths


STM_CONFIG_PATH = documents = os.path.join(userpaths.get_my_documents(), '__stamina__')
STAMINA_VERSION ='0.0.26'


class dcc(Enum):
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