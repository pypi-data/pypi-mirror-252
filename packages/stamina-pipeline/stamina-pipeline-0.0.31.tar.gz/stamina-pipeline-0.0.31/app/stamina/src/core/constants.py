from enum import Enum
import os
import userpaths

from ..core import utils

STM_CONFIG_PATH = documents = os.path.join(userpaths.get_my_documents(), '__stamina__')
STM_ICON_PATH = utils.fix_path(os.path.join(STM_CONFIG_PATH, 'resources/icons'))
STM_FEATHER_LIGHT_PATH = utils.fix_path(os.path.join(STM_ICON_PATH, 'feather-light'))
STM_VERSION ='0.0.31'
STM_PACKAGE_NAME = 'stamina-pipeline'


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
    authentication = 2


    accept_authentication = -1
    refuse_authentication = -2