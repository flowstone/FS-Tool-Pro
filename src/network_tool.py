import sys
import os

from PyQt5.QtWidgets import QApplication, QGroupBox, QRadioButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, \
    QPushButton, QFileDialog, QMessageBox, QTabWidget, QMainWindow
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from loguru import logger

from src.const.color_constants import BLACK
from src.ip_tool import IpToolApp
from src.port_killer import PortKillerApp
from src.port_scanner import PortScannerApp
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants

class NetworkToolApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.NETWORK_TOOL_WINDOW_TITLE} ----")
        self.setWindowTitle(FsConstants.NETWORK_TOOL_WINDOW_TITLE)
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
        self.tab_widget.addTab(IpToolApp(), "IP信息")
        self.tab_widget.addTab(PortScannerApp(), "端口扫描")
        self.tab_widget.addTab(PortKillerApp(), "端口关闭")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = NetworkToolApp()
    window.show()
    sys.exit(app.exec_())