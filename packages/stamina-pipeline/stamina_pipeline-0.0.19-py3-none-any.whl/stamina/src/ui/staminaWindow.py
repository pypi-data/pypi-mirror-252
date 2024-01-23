from ..core.logging import log
from ..core import config
from ..core import enums
from ..core.socketUtils import disconnect
from ..core import utils

import subprocess, userpaths, os, json
from PySide2.QtWidgets import *


APP = enums.apps.Desktop
STM_CONFIG_PATH = documents = os.path.join(userpaths.get_my_documents(), '__stamina__')


def get_config():
    with open(os.path.join(STM_CONFIG_PATH, 'config.json'), 'r+') as f:
        config_str = f.read()
        config = json.loads(config_str)
        return config


class window(QWidget):
    def __init__(self):
        super().__init__()

        self.setGeometry(0, 0, 100, 200)
        self.setWindowTitle('Stamina')


def main():
    log(f'Stamina Desktop Started! Version: {config.STAMINA_VERSION}')

    app = QApplication()
    stm_window = window()
    stm_window.show()
    app.exec_()

    disconnect()


if __name__ == '__main__':
    main()

# main()