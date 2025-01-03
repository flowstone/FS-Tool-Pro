import sys
import os
import socket
import threading

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QFileDialog, QListWidget, QSplitter
)
from PyQt5.QtCore import Qt, QThread, pyqtSignal

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from loguru import logger

BROADCAST_PORT = 9000
TRANSFER_PORT = 9001
BUFFER_SIZE = 4096


class BroadcastListenerThread(QThread):
    device_discovered = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.running = True
        self.udp_socket = None

    def run(self):
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.udp_socket.bind(("", BROADCAST_PORT))

        while self.running:
            try:
                data, addr = self.udp_socket.recvfrom(1024)
                message = data.decode("utf-8")
                if message.startswith("DISCOVER"):
                    self.device_discovered.emit(addr[0])
            except OSError as e:
                if self.running:  # 避免在关闭后打印错误
                    logger.error(f"Error: {e}")
            except Exception as e:
                logger.error(f"Error: {e}")

    def stop(self):
        self.running = False
        if self.udp_socket:
            self.udp_socket.close()
        self.quit()


class ServerThread(QThread):
    new_message = pyqtSignal(str)

    def __init__(self, save_dir="received_files"):
        super().__init__()
        self.save_dir = save_dir
        os.makedirs(save_dir, exist_ok=True)
        self.running = True
        self.server_socket = None

        # 获取本机 IP
        self.local_ip = self.get_local_ip()

    @staticmethod
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))  # 使用公网 IP 测试本地地址
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logger.warning(f"{e}")
            return "127.0.0.1"

    def run(self):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind(("", TRANSFER_PORT))
        self.server_socket.listen(5)

        self.new_message.emit("服务器已启动，等待连接...")
        logger.info("服务器已启动，等待连接...")
        self.new_message.emit(f"本机IP: {self.local_ip}, 端口: {TRANSFER_PORT}")
        logger.info(f"本机IP: {self.local_ip}, 端口: {TRANSFER_PORT}")
        self.new_message.emit(f"存储路径: {self.save_dir}")
        logger.info(f"存储路径: {self.save_dir}")

        while self.running:
            try:
                client_socket, addr = self.server_socket.accept()
                threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()
            except OSError as e:
                if self.running:  # 避免在关闭后打印错误
                    logger.error(f"Error: {e}")
            except Exception as e:
                self.new_message.emit(f"服务器错误: {e}")
                logger.error(f"服务器错误: {e}")
                break

    def handle_client(self, client_socket, addr):
        try:
            # 接收数据类型 (TEXT 或 FILE)
            raw_data = client_socket.recv(1024)
            try:
                data_type = raw_data.decode("utf-8").strip()
            except UnicodeDecodeError:
                self.new_message.emit(f"[{addr[0]}]: 无效的 UTF-8 数据")
                return

            if data_type == "TEXT":
                # 如果是文本消息，继续接收文本内容
                raw_text = client_socket.recv(4096)
                try:
                    text = raw_text.decode("utf-8")
                except UnicodeDecodeError:
                    self.new_message.emit(f"[{addr[0]}]: 无效的 UTF-8 文本内容")
                    return
                self.new_message.emit(f"[{addr[0]}]: {text}")

            elif data_type == "FILE":
                # 接收文件名，直到换行符为止
                filename_raw = b""
                while True:
                    chunk = client_socket.recv(1)  # 按字节接收，直到遇到换行符
                    if not chunk or chunk == b"\n":
                        break
                    filename_raw += chunk
                filename = filename_raw.decode("utf-8").strip()

                # 确保保存目录存在
                file_path = os.path.join(self.save_dir, filename)
                os.makedirs(self.save_dir, exist_ok=True)

                # 接收文件数据
                with open(file_path, "wb") as f:
                    while True:
                        chunk = client_socket.recv(BUFFER_SIZE)
                        if not chunk:
                            break
                        f.write(chunk)

                self.new_message.emit(f"[{addr[0]}]: {os.path.basename(file_path)}")
                logger.info(f"[{addr[0]}]: {os.path.basename(file_path)}")
        except Exception as e:
            self.new_message.emit(f"客户端错误: {e}")
            logger.warning(f"客户端错误: {e}")
        finally:
            client_socket.close()

    def stop(self):
        self.running = False
        if self.server_socket:
            self.server_socket.close()
        self.quit()


class FastSenderApp(QWidget):
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

        self.devices = set()
        self.broadcast_listener = BroadcastListenerThread()
        self.broadcast_listener.device_discovered.connect(self.add_device)
        self.broadcast_listener.start()

        self.server_thread = ServerThread(CommonUtil.get_fast_sender_dir())
        self.server_thread.new_message.connect(self.log_message)
        self.server_thread.start()
        self.start_broadcast_discovery()

    def start_broadcast_discovery(self):
        def broadcast_discovery():
            udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            while self.broadcast_running:
                udp_socket.sendto(b"DISCOVER", ("<broadcast>", BROADCAST_PORT))
                threading.Event().wait(5)

        self.broadcast_running = True
        self.broadcast_thread = threading.Thread(target=broadcast_discovery, daemon=True)
        self.broadcast_thread.start()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_FILE_COMPARATOR} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_FAST_SENDER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setGeometry(100, 100, 800, 600)

        title_label = QLabel(FsConstants.WINDOW_TITLE_FAST_SENDER)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)

        # 左侧设备列表
        self.device_list = QListWidget(self)
        self.device_list_label = QLabel("发现的设备:")

        device_layout = QVBoxLayout()
        device_layout.addWidget(self.device_list_label)
        device_layout.addWidget(self.device_list)

        # 右侧日志区
        self.log_area = QTextEdit(self)
        self.log_area.setReadOnly(True)
        log_layout = QVBoxLayout()
        log_layout.addWidget(QLabel("日志:"))
        log_layout.addWidget(self.log_area)

        # 使用 QSplitter 分割设备列表和日志
        splitter = QSplitter(Qt.Horizontal, self)
        splitter.addWidget(self.wrap_in_widget(device_layout))
        splitter.addWidget(self.wrap_in_widget(log_layout))
        splitter.setSizes([200, 600])  # 初始分割比例

        # 底部输入区
        self.message_input = QTextEdit(self)
        self.message_input.setPlaceholderText("输入文本消息...")

        self.send_text_button = QPushButton("发送文本", self)
        self.send_text_button.clicked.connect(self.send_text)

        self.send_file_button = QPushButton("发送文件", self)
        self.send_file_button.clicked.connect(self.send_file)

        # 按钮水平布局
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.send_text_button)
        button_layout.addWidget(self.send_file_button)

        # 整体输入区垂直布局
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.message_input)
        input_layout.addLayout(button_layout)

        # 整体布局
        main_layout = QVBoxLayout()

        main_layout.addWidget(title_label)
        main_layout.addWidget(splitter)
        main_layout.addLayout(input_layout)

        self.setLayout(main_layout)

    @staticmethod
    def wrap_in_widget(layout):
        """将布局包装到 QWidget 中，用于 QSplitter"""
        widget = QWidget()
        widget.setLayout(layout)
        return widget

    def add_device(self, ip):
        # 如果发现的 IP 是自己的 IP，直接忽略
        if ip == self.server_thread.local_ip:
            return
        if ip not in self.devices:
            self.devices.add(ip)
            self.device_list.addItem(ip)
            self.log_message(f"发现新设备: {ip}")
            logger.info(f"发现新设备: {ip}")

    def send_text(self):
        selected_ip = self.get_selected_device()
        if not selected_ip:
            return

        text = self.message_input.toPlainText().strip()
        if not text:
            self.log_message("文本消息不能为空！")
            logger.warning("文本消息不能为空！")
            return
        try:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((selected_ip, TRANSFER_PORT))
            logger.info(f"连接成功：{selected_ip} ({TRANSFER_PORT})")
            client_socket.sendall(b"TEXT")
            client_socket.sendall(text.encode("utf-8"))
            self.log_message(f"[{selected_ip}]: {text}")
            logger.info(f"[{selected_ip}]: {text}")
        except Exception as e:
            self.log_message(f"发送失败: {e}")
            logger.warning(f"发送失败: {e}")
        finally:
            client_socket.close()

    def send_file(self):
        selected_ip = self.get_selected_device()
        if not selected_ip:
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "选择文件")
        if not file_path:
            return

        try:
            filename = os.path.basename(file_path)
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((selected_ip, TRANSFER_PORT))
            logger.info(f"连接成功：{selected_ip} ({TRANSFER_PORT})")

            client_socket.sendall(b"FILE")
            client_socket.sendall((filename + "\n").encode("utf-8"))

            with open(file_path, "rb") as f:
                while chunk := f.read(BUFFER_SIZE):
                    client_socket.sendall(chunk)

            self.log_message(f"[{selected_ip}]: {filename}")
            logger.info(f"[{selected_ip}]: {filename}")
        except Exception as e:
            self.log_message(f"文件发送失败: {e}")
            logger.error(f"文件发送失败: {e}")
        finally:
            client_socket.close()

    def get_selected_device(self):
        selected_items = self.device_list.selectedItems()
        if not selected_items:
            self.log_message("未选择设备！")
            logger.info("未选择设备！")
            return None
        return selected_items[0].text()

    def log_message(self, message):
        self.log_area.append(message)

    def closeEvent(self, event):
        self.broadcast_running = False  # 停止广播线程
        # 停止其他后台线程
        self.broadcast_listener.stop()
        self.server_thread.stop()
        # 触发关闭信号（如果需要）
        self.closed_signal.emit()
        # 调用父类关闭事件
        super().closeEvent(event)


if __name__ == "__main__":

    app = QApplication(sys.argv)
    window = FastSenderApp()
    window.show()

    sys.exit(app.exec_())