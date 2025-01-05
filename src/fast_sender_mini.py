import logging
import os
import sys
import subprocess
from threading import Thread

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel
from PySide6.QtCore import Qt, Signal, QTimer, QThread
from loguru import logger

from src.const.color_constants import BLACK, BLUE
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil



class FastSenderMiniApp(QWidget):
    closed_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

        # Flask 服务进程和队列
        self.flask_process = None

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_FAST_SENDER_MINI} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_FAST_SENDER_MINI)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        # 创建布局
        self.layout = QVBoxLayout()

        title_label = QLabel(FsConstants.WINDOW_TITLE_FAST_SENDER_MINI)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        self.layout.addWidget(title_label)

        # 说明文本
        description_label = QLabel("一个轻量级服务，通过浏览器上传文本/文件，分享给其它设备")
        description_label.setFont(FontConstants.ITALIC_SMALL)
        self.layout.addWidget(description_label)

        # 创建日志框
        self.log_text = QTextEdit(self)
        self.log_text.setReadOnly(True)
        self.layout.addWidget(QLabel("日志"))
        self.layout.addWidget(self.log_text)

        # 创建按钮
        self.start_button = QPushButton("启动服务", self)
        self.start_button.clicked.connect(self.start_flask)
        self.stop_button = QPushButton("停止服务", self)
        self.stop_button.setEnabled(False)  # 禁用关闭按钮
        self.stop_button.clicked.connect(self.stop_flask)

        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        self.layout.addLayout(button_layout)
        self.setLayout(self.layout)

    def start_flask(self):
        """启动 Flask 服务进程"""
        if self.flask_process is None or self.flask_process.poll() is not None:  # 如果进程已经结束或为空
            self.log("正在启动 Flask 服务...")
            # 启动 Flask 服务的子进程
            self.flask_process = subprocess.Popen(
                [sys.executable, 'flask_server.py'],  # 启动 Flask 服务文件，确保路径正确
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            self.log("Flask 服务已启动。")
            self.log(f"服务器根目录: {CommonUtil.get_flask_mini_dir()}")
            self.log("127.0.0.1:5678")
            self.log(f"{CommonUtil.get_local_ip()}:5678")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        else:
            self.log("Flask 服务已经在运行中。")


    def stop_flask(self):
        """停止 Flask 服务"""
        if self.flask_process and self.flask_process.poll() is None:
            self.log("正在停止 Flask 服务...")
            self.flask_process.terminate()  # 终止 Flask 服务
            self.flask_process = None
            self.log("Flask 服务已停止。")
        else:
            self.log("Flask 服务没有运行。")
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)


    def log(self, message):
        """记录日志信息到文本框"""
        logger.info(message)
        self.log_text.append(message)

    def closeEvent(self, event):
        """关闭窗口时确保 Flask 服务停止"""
        self.stop_flask()
        # 触发关闭信号（如果需要）
        self.closed_signal.emit()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FastSenderMiniApp()
    window.show()
    sys.exit(app.exec())
