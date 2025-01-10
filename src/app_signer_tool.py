import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QTabWidget
)
from loguru import logger

from src.app_signer import AppSignerApp
from src.app_signer_generate_certificate import GenerateCertificateApp
from src.app_signer_public_key_extractor import PublicKeyExtractorApp
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.tabwidget_animation import AnimatedTabWidget


class AppSignerTool(QWidget):
    closed_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_APP_SIGNER_TOOL} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_APP_SIGNER_TOOL)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setMinimumWidth(700)
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)

        # 创建主布局
        layout = QVBoxLayout(self)
        # 创建 TabWidget
        self.tab_widget = AnimatedTabWidget()
        # 添加标签页
        self.add_tabs()
        # 将 TabWidget 添加到布局
        layout.addWidget(self.tab_widget)
        # 设置主窗口布局
        self.setLayout(layout)

    def add_tabs(self):
        self.tab_widget.addTab(AppSignerApp(), "文件签名")
        self.tab_widget.addTab(GenerateCertificateApp(), "证书生成")
        self.tab_widget.addTab(PublicKeyExtractorApp(), "证书转换")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = AppSignerTool()
    window.show()
    sys.exit(app.exec())