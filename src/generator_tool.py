import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from fs_base.widget import TabAnimation
from loguru import logger

from src.const.fs_constants import FsConstants
from src.password_generator import PasswordGeneratorApp
from src.person_password_generator import PersonPasswordGeneratorApp
from src.rsa_key_generator import RSAKeyGeneratorApp
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class GeneratorToolApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_GENERATOR_TOOL} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_GENERATOR_TOOL)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        #self.setFixedHeight(500)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)

        # 创建主布局
        layout = QVBoxLayout(self)
        # 创建 TabWidget
        self.tab_widget = TabAnimation()
        # 添加标签页
        self.add_tabs()
        # 将 TabWidget 添加到布局
        layout.addWidget(self.tab_widget)
        # 设置主窗口布局
        self.setLayout(layout)


    def add_tabs(self):
        self.tab_widget.addTab(PasswordGeneratorApp(), "密码生成")
        self.tab_widget.addTab(PersonPasswordGeneratorApp(), "个性密码生成")
        self.tab_widget.addTab(RSAKeyGeneratorApp(), "RSA生成")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GeneratorToolApp()
    window.show()
    sys.exit(app.exec())