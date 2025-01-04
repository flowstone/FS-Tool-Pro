import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from loguru import logger

from src.const.fs_constants import FsConstants
from src.image_convert import ImageConvertApp
from src.image_heic_jpg import HeicToJpgApp
from src.preferences_about import PreferencesAbout
from src.preferences_general import PreferencesGeneral
from src.util.common_util import CommonUtil


class Preferences(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.PREFERENCES_WINDOW_TITLE} ----")
        self.setWindowTitle(FsConstants.PREFERENCES_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)

        # 创建主布局
        layout = QVBoxLayout(self)
        # 创建 TabWidget
        self.tab_widget = QTabWidget()
        # 添加标签页
        self.add_tabs()
        # 将 TabWidget 添加到布局
        layout.addWidget(self.tab_widget)
        # 设置主窗口布局
        self.setLayout(layout)


    def add_tabs(self):
        self.tab_widget.addTab(PreferencesGeneral(), FsConstants.PREFERENCES_WINDOW_TITLE_GENERAL)
        self.tab_widget.addTab(PreferencesAbout(), FsConstants.PREFERENCES_WINDOW_TITLE_ABOUT)

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Preferences()
    window.show()
    sys.exit(app.exec_())