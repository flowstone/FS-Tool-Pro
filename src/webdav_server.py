from PySide6.QtGui import QIcon, Qt
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QMessageBox, QLineEdit, QTextEdit, QFileDialog, QHBoxLayout
)
from PySide6.QtCore import QThread, Signal
from fs_base.message_util import MessageUtil
from loguru import logger
from wsgidav.wsgidav_app import WsgiDAVApp
from cheroot import wsgi
import os
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class WebDAVThread(QThread):
    # 自定义信号
    log_signal = Signal(str)
    started_signal = Signal()
    stopped_signal = Signal()

    def __init__(self, host, port, root_path):
        super().__init__()
        self.host = host
        self.port = port
        self.root_path = root_path
        self.server = None

    def run(self):
        try:
            # 配置 WsgiDAV 服务
            config = {
                "host": self.host,
                "port": self.port,
                "provider_mapping": {"/": self.root_path},
                "verbose": 1,
                "simple_dc": {"user_mapping": {"*": True}},
                "http_authenticator": {
                    "accept_basic": True,
                    "default_to_digest": False,
                },
            }

            self.log_signal.emit(f"启动 WebDAV 服务\n根目录：{self.root_path}\n地址：http://{CommonUtil.get_local_ip()}:{self.port}")
            dav_app = WsgiDAVApp(config)
            self.server = wsgi.Server((self.host, self.port), dav_app)

            self.started_signal.emit()
            self.server.start()
        except Exception as e:
            self.log_signal.emit(f"WebDAV 服务出错：{e}")
        finally:
            if self.server:
                self.server.stop()
            self.stopped_signal.emit()

    def stop(self):
        if self.server:
            self.server.stop()
            self.terminate()
            self.log_signal.emit("WebDAV 服务已停止")


class WebDAVServerApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.webdav_thread = None

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_WEBDAV_SERVER} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_WEBDAV_SERVER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setFixedWidth(600)

        # 界面组件
        title_label = QLabel(FsConstants.WINDOW_TITLE_WEBDAV_SERVER)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")

        self.label_root_path = QLabel("根目录：", self)
        folder_layout = QHBoxLayout()
        self.input_root_path = QLineEdit(self)
        self.button_browse = QPushButton("选择目录", self)
        folder_layout.addWidget(self.input_root_path)
        folder_layout.addWidget(self.button_browse)
        self.label_port = QLabel("端口号：", self)
        self.input_port = QLineEdit(self)
        self.input_port.setText("9002")  # 默认端口号
        button_layout = QHBoxLayout()

        self.button_start = QPushButton("启动服务", self)
        self.button_stop = QPushButton("停止服务", self)
        button_layout.addWidget(self.button_start)
        button_layout.addWidget(self.button_stop)
        self.button_stop.setEnabled(False)

        self.text_log = QTextEdit(self)
        self.text_log.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.label_root_path)
        layout.addLayout(folder_layout)
        layout.addWidget(self.label_port)
        layout.addWidget(self.input_port)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel("日志输出："))
        layout.addWidget(self.text_log)
        #layout.addWidget(TransparentTextBox())
        self.setLayout(layout)

        # 绑定事件
        self.button_browse.clicked.connect(self.browse_directory)
        self.button_start.clicked.connect(self.start_server)
        self.button_stop.clicked.connect(self.stop_server)

    def browse_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择根目录")
        if directory:
            self.input_root_path.setText(directory)

    def start_server(self):
        root_path = self.input_root_path.text().strip()
        port_text = self.input_port.text().strip()

        if not root_path:
            logger.warning("请指定根目录")
            MessageUtil.show_warning_message("请指定根目录")
            return

        if not port_text.isdigit():
            logger.warning("端口号必须是数字")
            MessageUtil.show_warning_message("端口号必须是数字")
            return

        port = int(port_text)
        if port <= 0 or port > 65535:
            logger.warning("端口号必须在 1-65535 范围内")
            MessageUtil.show_warning_message("端口号必须在 1-65535 范围内")
            return

        if not os.path.exists(root_path):
            logger.warning("指定的根目录不存在")
            MessageUtil.show_warning_message("指定的根目录不存在")
            return

        self.webdav_thread = WebDAVThread("0.0.0.0", port, root_path)
        self.webdav_thread.log_signal.connect(self.append_log)
        self.webdav_thread.started_signal.connect(self.on_server_started)
        self.webdav_thread.stopped_signal.connect(self.on_server_stopped)

        try:
            self.webdav_thread.start()
        except Exception as e:
            logger.error(f"启动服务失败: {e}")
            MessageUtil.show_error_message(f"启动服务失败: {e}")

    def stop_server(self):
        if self.webdav_thread and self.webdav_thread.isRunning():
            self.webdav_thread.stop()
            self.webdav_thread.wait()

    def on_server_started(self):
        self.button_start.setEnabled(False)
        self.button_stop.setEnabled(True)

    def on_server_stopped(self):
        self.button_start.setEnabled(True)
        self.button_stop.setEnabled(False)

    def append_log(self, message):
        self.text_log.append(message)


if __name__ == "__main__":
    app = QApplication([])

    window = WebDAVServerApp()
    window.show()

    app.exec()
