import socket
import sys
from concurrent.futures import ThreadPoolExecutor

import psutil
from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit, QHBoxLayout, QCheckBox
)
from loguru import logger

from src.const.color_constants import BLACK, BLUE
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.util.permission_util import PermissionUtil
from src.widget.custom_progress_widget import CustomProgressBar
from src.widget.sub_window_widget import SubWindowWidget


def scan_port(ip, port):
    """
    扫描单个端口
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.05)
            if s.connect_ex((ip, port)) == 0:
                return port
    except Exception as e:
        print(f"Error scanning port {port}: {e}")
        return None


def get_open_ports(target_ip, ports, progress_callback, error_callback):
    """
    扫描指定 IP 的端口
    """
    open_ports = []
    total_ports = len(ports)
    progress = 0

    try:
        with ThreadPoolExecutor(max_workers=50) as executor:
            futures = [
                executor.submit(scan_port, target_ip, port)
                for port in ports
            ]
            for i, future in enumerate(futures):
                result = future.result()
                if result is not None:
                    open_ports.append(result)

                progress = int((i + 1) / total_ports * 100)
                progress_callback.emit(progress)

    except Exception as e:
        error_callback.emit(str(e))

    return open_ports


class PortScannerThread(QThread):
    progress_signal = Signal(int)
    result_signal = Signal(list)
    error_signal = Signal(str)

    def __init__(self, target_ip, ports):
        super().__init__()
        self.target_ip = target_ip
        self.ports = ports

    def run(self):
        open_ports = get_open_ports(
            self.target_ip, self.ports, self.progress_signal, self.error_signal
        )
        self.result_signal.emit(open_ports)


class PortKillerApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IP_INFO_PORT_KILLER} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_IP_INFO_PORT_KILLER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.layout = QVBoxLayout(self)

        title_label = QLabel(FsConstants.WINDOW_TITLE_IP_INFO_PORT_KILLER)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        self.layout.addWidget(title_label)

        self.description_label = QLabel("输入目标 IP 和端口范围，点击搜索按钮查看被占用的端口")

        self.ip_input_label = QLabel("目标 IP 地址:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("例如: 127.0.0.1")
        self.ip_input.setText("127.0.0.1")

        self.specific_checkbox = QCheckBox("指定单个端口")
        self.specific_checkbox.setChecked(True)
        self.specific_checkbox.toggled.connect(self.toggle_input_mode)
        # 复选框
        self.range_checkbox = QCheckBox("使用端口范围")
        self.range_checkbox.toggled.connect(self.toggle_input_mode)

        self.specific_port_label = QLabel("单个端口:")
        self.specific_port_input = QLineEdit()
        self.specific_port_input.setPlaceholderText("例如: 80")

        self.port_input_label = QLabel("端口范围 (起始-结束):")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 1-65535")
        self.port_input.setText("1-65535")
        self.port_input_label.hide()
        self.port_input.hide()



        button_layout = QHBoxLayout()
        self.admin_button = QPushButton("授权")
        self.admin_button.clicked.connect(self.get_admin)

        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_ports)

        self.kill_button = QPushButton("停止")
        self.kill_button.clicked.connect(self.kill_port)

        if CommonUtil.check_mac_os():
            button_layout.addWidget(self.admin_button)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.kill_button)

        self.port_list = QListWidget()

        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.ip_input_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.specific_checkbox)
        self.layout.addWidget(self.range_checkbox)
        self.layout.addWidget(self.port_input_label)
        self.layout.addWidget(self.port_input)
        self.layout.addWidget(self.specific_port_label)
        self.layout.addWidget(self.specific_port_input)
        self.layout.addLayout(button_layout)

        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.port_list)

    def toggle_input_mode(self):
        """确保复选框互斥，并切换输入模式"""
        if self.sender() == self.range_checkbox and self.range_checkbox.isChecked():
            self.specific_checkbox.setChecked(False)
            self.port_input_label.show()
            self.port_input.show()
            self.specific_port_label.hide()
            self.specific_port_input.hide()
        elif self.sender() == self.specific_checkbox and self.specific_checkbox.isChecked():
            self.range_checkbox.setChecked(False)
            self.port_input_label.hide()
            self.port_input.hide()
            self.specific_port_label.show()
            self.specific_port_input.show()

    def get_admin(self):
        """获得管理员权限"""
        PermissionUtil.check_admin()

    def search_ports(self):
        """搜索被占用的端口"""
        self.port_list.clear()
        self.progress_bar.setValue(0)

        target_ip = self.ip_input.text().strip()

        ports = []
        if self.range_checkbox.isChecked():
            port_range = self.port_input.text().strip()
            try:
                start_port, end_port = map(int, port_range.split("-"))
                if start_port < 1 or end_port > 65535 or start_port > end_port:
                    raise ValueError
                ports = range(start_port, end_port + 1)
            except ValueError:
                MessageUtil.show_warning_message("端口范围格式不正确，请输入有效范围 (例如: 1-1000)！")
                return
        elif self.specific_checkbox.isChecked():
            try:
                port = int(self.specific_port_input.text().strip())
                if port < 1 or port > 65535:
                    raise ValueError
                ports = [port]
            except ValueError:
                MessageUtil.show_warning_message("单个端口格式不正确，请输入有效端口 (例如: 80)！")
                return

        self.description_label.setText("正在扫描端口，请稍候...")
        self.search_button.setEnabled(False)
        self.scanner_thread = PortScannerThread(target_ip, ports)
        self.scanner_thread.progress_signal.connect(self.progress_bar.update_progress)
        self.scanner_thread.result_signal.connect(self.display_ports)
        self.scanner_thread.error_signal.connect(self.display_error)
        self.scanner_thread.start()
        self.progress_bar.show()

    def display_ports(self, open_ports):
        """显示被占用端口"""
        self.search_button.setEnabled(True)
        self.progress_bar.hide()
        if open_ports:
            self.description_label.setText("选择一个端口，然后点击停止按钮杀死对应的进程。")
            for port in open_ports:
                self.port_list.addItem(f"端口: {port}")
        else:
            self.description_label.setText("未找到被占用的端口。")

    def display_error(self, error_message):
        """显示错误信息"""
        self.progress_bar.hide()
        self.search_button.setEnabled(True)
        MessageUtil.show_error_message(error_message)

    def kill_port(self):
        """停止选中端口对应的进程"""
        selected_item = self.port_list.currentItem()
        if not selected_item:
            MessageUtil.show_warning_message("请先选择一个端口！")
            return

        selected_text = selected_item.text()
        try:
            port = int(selected_text.split(":")[1].strip())
        except (IndexError, ValueError):
            MessageUtil.show_warning_message("无法解析选中的端口信息。")
            return

        try:
            PermissionUtil.check_admin()
            for conn in psutil.net_connections(kind="inet"):
                if conn.laddr and conn.laddr.port == port:
                    pid = conn.pid
                    if pid:
                        psutil.Process(pid).terminate()
                        MessageUtil.show_success_message(f"端口 {port} 已被成功释放！")
                        self.search_ports()
                        return
        except psutil.AccessDenied:
            MessageUtil.show_error_message("操作被拒绝！请以管理员身份运行程序。")
            return
        except Exception as e:
            MessageUtil.show_error_message(f"无法终止进程：{str(e)}")
            return
        MessageUtil.show_warning_message(f"未能找到占用端口 {port} 的进程。")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    killer_app = PortKillerApp()
    killer_app.show()
    sys.exit(app.exec())
