import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from loguru import logger

from src.const.fs_constants import FsConstants
from src.fast_sender import FastSenderApp
from src.fast_sender_mini import FastSenderMiniApp
from src.util.common_util import CommonUtil


class FastSenderToolApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_FAST_SENDER_TOOL} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_FAST_SENDER_TOOL)
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
        self.tab_widget.addTab(FastSenderApp(), "文件传输")
        self.tab_widget.addTab(FastSenderMiniApp(), "Mini服务")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FastSenderToolApp()
    window.show()
    sys.exit(app.exec_())