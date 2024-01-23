from ..core.logging import log
from ..core import config
from ..core import constants
from ..core.socketUtils import disconnect, send
from ..core import utils

import subprocess, userpaths, os, json
from PySide2.QtWidgets import *
from PySide2 import QtCore
from PySide2 import QtGui


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



        conn_w = self.connection_widget()
        body_w = self.body_widget()

        self.main_stacked = QStackedWidget()
        self.main_stacked.addWidget(conn_w)
        self.main_stacked.addWidget(body_w)

        # SETUP
        self.setGeometry(800, 200, 400, 700)
        self.setWindowTitle('Stamina')
        icon_path = utils.fix_path(os.path.join(os.path.abspath(os.getcwd()), 'app/stamina/src/resources/icons/stamina.png'))
        self.setWindowIcon(QtGui.QIcon(icon_path))

        print(os.getcwd())
        self.lyt = QVBoxLayout(self)
        self.lyt.setContentsMargins(0, 0, 0, 0)
        self.lyt.addWidget(self.main_stacked)

    def __del__(self):
        disconnect()

    def connect_event(self):
        answer = send(
            constants.messageTypes.authentication,
        {
                'username': self.username_ln.text(),
                'password': self.password_ln.text()
            }

        )
        answer = constants.messageTypes(int(answer))
        if answer == constants.messageTypes.accept_authentication:
            self.main_stacked.setCurrentIndex(1)
        else:
            self.error_lb.setText('Wrong password or username,\nauthentication refused.')

    def connection_widget(self):
        self.username_ln = QLineEdit()
        self.username_ln.setStyleSheet("""padding-left:10; padding-right: 10px""")
        self.username_ln.setPlaceholderText('Username')
        self.username_ln.setFixedSize(QtCore.QSize(200, 30))
        self.password_ln = QLineEdit()
        self.password_ln.setStyleSheet("""padding-left:10; padding-right: 10px""")
        self.password_ln.setPlaceholderText('Password')
        self.password_ln.setFixedSize(QtCore.QSize(200, 30))
        self.username_ln.returnPressed.connect(lambda: self.password_ln.setFocus())
        self.password_ln.returnPressed.connect(self.connect_event)
        btn = QPushButton('Connect')
        btn.clicked.connect(self.connect_event)
        btn.setFixedSize(QtCore.QSize(200, 30))
        self.error_lb = QLabel('')
        self.error_lb.setStyleSheet("""color: red;""")


        lyt = QVBoxLayout()
        lyt.setAlignment(QtCore.Qt.AlignHCenter)
        lyt.addStretch()
        lyt.addWidget(self.username_ln)
        lyt.addWidget(self.password_ln)
        lyt.addWidget(btn)
        lyt.addWidget(self.error_lb)
        lyt.addStretch()
        widget = QWidget()
        widget.setLayout(lyt)

        return widget

    @staticmethod
    def body_widget():

        l = QVBoxLayout()
        w = QWidget()
        w.setLayout(l)

        return w


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
