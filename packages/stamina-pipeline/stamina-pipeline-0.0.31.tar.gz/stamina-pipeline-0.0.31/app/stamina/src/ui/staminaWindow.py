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



        self.connection_tab()
        self.work_tab()

        self.main_stacked = QStackedWidget()
        self.main_stacked.addWidget(self.connection_tab_widget)
        self.main_stacked.addWidget(self.work_tab_widget)

        self.connection_btn.click()

        # SETUP
        self.setGeometry(800, 200, 400, 700)
        self.setWindowTitle('Stamina')
        self.setWindowIcon(QtGui.QIcon(utils.fix_path(os.path.join(constants.STM_ICON_PATH, 'stamina.png'))))
        # self.setStyleSheet("""QWidget{background-color: #292929;}""")

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

    def connection_tab(self):
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
        self.connection_btn = QPushButton('Connect')
        self.connection_btn.clicked.connect(self.connect_event)
        self.connection_btn.setFixedSize(QtCore.QSize(200, 30))
        self.error_lb = QLabel('')
        self.error_lb.setStyleSheet("""color: red;""")

        self.username_ln.setText('quentin-costagliola')
        self.password_ln.setText('123')



        lyt = QVBoxLayout()
        lyt.setAlignment(QtCore.Qt.AlignHCenter)
        lyt.addStretch()
        lyt.addWidget(self.username_ln)
        lyt.addWidget(self.password_ln)
        lyt.addWidget(self.connection_btn)
        lyt.addWidget(self.error_lb)
        lyt.addStretch()
        self.connection_tab_widget = QWidget()
        self.connection_tab_widget.setLayout(lyt)


    def menu_bar(self):

        select_project_combo = QComboBox()
        select_project_combo.setFixedWidth(150)
        select_project_combo.addItem('Project 1')
        select_project_combo.addItem('Project 2...')

        create_proj_btn = QToolButton()
        create_proj_btn.setIcon(QtGui.QIcon(utils.fix_path(os.path.join(constants.STM_FEATHER_LIGHT_PATH, 'plus-circle.svg'))))
        print(utils.fix_path(os.path.join(constants.STM_FEATHER_LIGHT_PATH, 'create_proj.svg')))
        join_proj_btn = QToolButton()
        join_proj_btn.setIcon(QtGui.QIcon(utils.fix_path(os.path.join(constants.STM_FEATHER_LIGHT_PATH, 'log-in.svg'))))
        remove_proj_btn = QToolButton()
        remove_proj_btn.setIcon(QtGui.QIcon(utils.fix_path(os.path.join(constants.STM_FEATHER_LIGHT_PATH, 'x-circle.svg'))))

        lyt = QHBoxLayout()
        lyt.setContentsMargins(0, 0, 0, 0)
        lyt.addWidget(select_project_combo)
        lyt.addWidget(create_proj_btn)
        lyt.addWidget(join_proj_btn)
        lyt.addWidget(remove_proj_btn)
        lyt.addStretch()
        widget = QWidget()
        widget.setLayout(lyt)

        return widget

    def body_splitter(self):

        self.body_splitter = QSplitter()
        self.body_splitter.setOrientation(QtCore.Qt.Vertical)

        self.local_model = QFileSystemModel()
        self.local_model.setRootPath(QtCore.QDir.currentPath())
        self.local_tree = QTreeView(self)
        # self.local_tree.setHeaderHidden(True)
        self.local_tree.setColumnHidden(1, True)
        self.local_tree.setColumnHidden(3, 1)
        self.local_tree.setModel(self.local_model)
        # local_tree.setRootIndex(local_model.index(r'D:/'))
        self.remote_model = QFileSystemModel()
        self.remote_model.setRootPath(r'F:\applied_houdini-liquidsII')
        print(self.remote_model.rootPath())
        self.remote_tree = QTreeView(self)
        self.remote_tree.setModel(self.remote_model)

        self.body_splitter.addWidget(self.local_tree)
        self.body_splitter.addWidget(self.remote_tree)


    def work_tab(self):

        menu_bar = self.menu_bar()
        self.body_splitter()

        margins= 5
        lyt = QVBoxLayout()
        lyt.setContentsMargins(margins, margins, margins, margins)
        lyt.addWidget(menu_bar)
        lyt.addWidget(self.body_splitter)
        # lyt.addStretch()
        self.work_tab_widget = QWidget()
        self.work_tab_widget.setLayout(lyt)


def run():
    log(f'Stamina is starting with version: {constants.STM_VERSION}')

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
