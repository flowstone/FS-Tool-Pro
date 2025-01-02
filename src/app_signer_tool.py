import sys

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget
)
from loguru import logger

from src.app_signer import AppSignerApp
from src.app_signer_generate_certificate import GenerateCertificateApp
from src.app_signer_public_key_extractor import PublicKeyExtractorApp
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil


class AppSignerTool(QWidget):
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("应用程序签名工具")
        #self.setGeometry(200, 200, 700, 500)
        self.setFixedWidth(700)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.FILE_TOOL_WINDOW_TITLE} ----")
        self.setWindowTitle(FsConstants.APP_SIGNER_TOOL_WINDOW_TITLE)
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
        self.tab_widget.addTab(AppSignerApp(), FsConstants.APP_SIGNER_WINDOW_TITLE)
        self.tab_widget.addTab(GenerateCertificateApp(), FsConstants.GENERATE_CERTIFICATE_WINDOW_TITLE)
        self.tab_widget.addTab(PublicKeyExtractorApp(), FsConstants.PUBLIC_KEY_EXTRACTOR_WINDOW_TITLE)

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppSignerTool()
    window.show()
    sys.exit(app.exec_())