from ..core.logging import log
from ..core import config
from ..core import enums
from ..core.socketUtils import disconnect
from ..core import utils

import subprocess, userpaths, os, json
from PySide2.QtWidgets import *


APP = enums.dcc.Desktop
STM_CONFIG_PATH = documents = os.path.join(userpaths.get_my_documents(), '__stamina__')


def get_config():
    with open(os.path.join(STM_CONFIG_PATH, 'config.json'), 'r+') as f:
        config_str = f.read()
        config = json.loads(config_str)
        return config


def check_dcc():
    try:
        import maya
        return enums.dcc.Maya
    except ModuleNotFoundError:
        try:
            import hou
            return enums.dcc.Houdini
        except ModuleNotFoundError:
            return enums.dcc.Desktop


class window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 200, 400, 700)
        self.setWindowTitle('Stamina')

    def __del__(self):
        disconnect()


def run():
    log(f'Stamina is starting with version: {config.STAMINA_VERSION}')

    DCC = check_dcc()
    print(DCC)

    if DCC == enums.dcc.Desktop:
        app = QApplication()
        stm_window = window()
        stm_window.show()
        app.exec_()
    else:
        stm_window = window()
        return stm_window



if __name__ == '__main__':
    run()

# main()