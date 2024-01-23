from ..core.logging import log
from ..core import config
from ..core import constants
from ..core.socketUtils import disconnect
from ..core import utils

import subprocess, userpaths, os, json
from PySide2.QtWidgets import *


APP = constants.dcc.Desktop






def check_dcc():
    try:
        import maya
        return constants.dcc.Maya
    except ModuleNotFoundError:
        try:
            import hou
            return constants.dcc.Houdini
        except ModuleNotFoundError:
            return constants.dcc.Desktop


class window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(800, 200, 400, 700)
        self.setWindowTitle('Stamina')

    def __del__(self):
        disconnect()


def run():
    log(f'Stamina is starting with version: {constants .STAMINA_VERSION}')

    DCC = check_dcc()
    print(DCC)

    if DCC == constants.dcc.Desktop:
        app = QApplication()
        stm_window = window()
        stm_window.show()
        app.exec_()
    else:
        stm_window = window()
        return stm_window



if __name__ == '__main__':
    run()
