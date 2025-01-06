import sys
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QMenuBar, QMenu, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QSystemTrayIcon, QMenu
from src.const.fs_constants import FsConstants
import os
from src.util.common_util import CommonUtil
from loguru import logger


class LogStream:
    """自定义日志流，将输出重定向到 QTextEdit"""

    def __init__(self, text_edit):
        self.text_edit = text_edit

    def write(self, message):
        """将信息写入 QTextEdit 控件"""
        self.text_edit.append(message)

    def flush(self):
        """flush 方法用于兼容 sys.stdout"""
        pass


class LogWindow(QWidget):
    """日志窗口类"""

    def __init__(self):
        super().__init__()
        self.setWindowTitle("日志窗口")
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_FAST_SENDER_MINI} ----")
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setGeometry(0, 0, 800, 400)
        self.layout = QVBoxLayout(self)

        # 创建 QTextEdit 控件来显示日志
        self.log_text_edit = QTextEdit(self)
        self.log_text_edit.setReadOnly(True)

        self.layout.addWidget(self.log_text_edit)
        self.setLayout(self.layout)

        # 将日志输出到 QTextEdit
        sys.stdout = LogStream(self.log_text_edit)
        sys.stderr = LogStream(self.log_text_edit)
        logger.add(sys.stdout, level="INFO")
        logger.add(sys.stderr, level="ERROR")