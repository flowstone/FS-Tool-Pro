import socket
import sys
from concurrent.futures import ThreadPoolExecutor

from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QLineEdit, QCheckBox
)
from loguru import logger
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.custom_progress_widget import CustomProgressBar
from src.widget.sub_window_widget import SubWindowWidget


def scan_port(ip, port):
    """
    扫描单个端口
    """
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.05)  # 降低超时时间
            if s.connect_ex((ip, port)) == 0:
                return port
    except Exception as e:
        logger.error(f"Error scanning port {port}: {e}")  # 打印错误信息
        return None


def get_open_ports(target_ip, ports, progress_callback, error_callback):
    """
    扫描指定 IP 的端口，使用线程池并发
    """
    open_ports = []
    total_ports = len(ports)
    progress = 0

    try:
        with ThreadPoolExecutor(max_workers=50) as executor:  # 设置线程池大小
            futures = [
                executor.submit(scan_port, target_ip, port)
                for port in ports
            ]

            for i, future in enumerate(futures):
                result = future.result()
                if result is not None:
                    open_ports.append(result)

                # 更新进度条
                progress = int((i + 1) / total_ports * 100)
                progress_callback.emit(progress)

    except Exception as e:
        error_callback.emit(str(e))  # 捕获错误并通过信号传递错误信息

    return open_ports


class WorkerThread(QThread):
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
        if open_ports is not None:
            self.result_signal.emit(open_ports)


class PortScannerApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IP_INFO_PORT_SCANNER} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_IP_INFO_PORT_SCANNER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 主界面布局
        self.layout = QVBoxLayout(self)
        title_label = QLabel(FsConstants.WINDOW_TITLE_IP_INFO_PORT_SCANNER)
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        self.layout.addWidget(title_label)

        # 标题
        self.description_label = QLabel("输入目标 IP 和端口范围，点击按钮开始扫描")

        # 输入目标 IP
        self.ip_input_label = QLabel("目标 IP 地址:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("例如: 192.168.1.1")
        self.ip_input.setText("127.0.0.1")

        self.specific_checkbox = QCheckBox("指定单个端口")
        self.specific_checkbox.setChecked(True)
        self.specific_checkbox.toggled.connect(self.toggle_input_mode)

        # 添加复选框用于选择范围或单个端口
        self.range_checkbox = QCheckBox("使用端口范围")
        self.range_checkbox.toggled.connect(self.toggle_input_mode)


        # 输入端口范围
        self.port_input_label = QLabel("端口范围 (起始-结束):")
        self.port_input_label.hide()
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 1-65535")
        self.port_input.setText("1-65535")  # 设置默认值
        self.port_input.hide()
        # 输入单个端口
        self.specific_port_input_label = QLabel("单个端口:")
        self.specific_port_input = QLineEdit()
        self.specific_port_input.setPlaceholderText("例如: 80")
        #self.specific_port_input.hide()  # 默认隐藏

        # 扫描按钮
        self.scan_button = QPushButton("扫描打开的端口")
        self.scan_button.clicked.connect(self.scan_ports)

        # 显示结果
        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)

        # 添加进度条
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()

        # 布局
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.ip_input_label)
        self.layout.addWidget(self.ip_input)

        self.layout.addWidget(self.specific_checkbox)
        self.layout.addWidget(self.range_checkbox)

        self.layout.addWidget(self.port_input_label)
        self.layout.addWidget(self.port_input)

        self.layout.addWidget(self.specific_port_input_label)
        self.layout.addWidget(self.specific_port_input)

        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.result_box)

    def toggle_input_mode(self):
        """确保每次只能选择一个复选框，并切换输入模式"""
        if self.sender() == self.range_checkbox and self.range_checkbox.isChecked():
            self.specific_checkbox.setChecked(False)
            self.port_input.show()
            self.port_input_label.show()
            self.specific_port_input.hide()
            self.specific_port_input_label.hide()
        elif self.sender() == self.specific_checkbox and self.specific_checkbox.isChecked():
            self.range_checkbox.setChecked(False)
            self.port_input.hide()
            self.port_input_label.hide()
            self.specific_port_input.show()
            self.specific_port_input_label.show()

    def scan_ports(self):
        self.result_box.clear()
        self.progress_bar.setValue(0)  # 重置进度条

        target_ip = self.ip_input.text().strip()

        # 检查 IP 地址输入
        if not target_ip:
            self.result_box.append("错误: 请输入目标 IP 地址！")
            return

        ports = []
        ports_text = []

        if self.range_checkbox.isChecked():
            # 处理端口范围
            port_range = self.port_input.text().strip()
            try:
                start_port, end_port = map(int, port_range.split("-"))
                if start_port < 1 or end_port > 65535 or start_port > end_port:
                    raise ValueError
                ports = range(start_port, end_port + 1)
                ports_text = [start_port, end_port + 1]

            except ValueError:
                self.result_box.append("错误: 端口范围格式不正确，请输入有效范围 (例如: 1-1000)！")
                return
        elif self.specific_checkbox.isChecked():
            # 处理单个端口
            try:
                specific_port = int(self.specific_port_input.text().strip())
                if specific_port < 1 or specific_port > 65535:
                    raise ValueError
                ports = [specific_port]
                ports_text = [specific_port]
            except ValueError:
                self.result_box.append("错误: 单个端口格式不正确，请输入有效端口 (例如: 80)！")
                return
        else:
            self.result_box.append("错误: 请至少选择一种端口输入模式！")
            return

        self.description_label.setText("正在扫描端口，请稍候...")
        self.result_box.append(f"正在扫描目标 IP: {target_ip}，端口: {ports_text}...")
        self.result_box.append("这可能需要一些时间，请耐心等待。")
        self.scan_button.setEnabled(False)

        # 启动扫描线程
        self.worker_thread = WorkerThread(target_ip, ports)
        self.worker_thread.progress_signal.connect(self.progress_bar.update_progress)
        self.worker_thread.result_signal.connect(self.display_results)
        self.worker_thread.error_signal.connect(self.display_error)
        self.worker_thread.start()
        self.progress_bar.show()

    def display_results(self, open_ports):
        """显示扫描结果"""
        self.scan_button.setEnabled(True)
        self.progress_bar.hide()
        self.description_label.setText("扫描端口结束...")

        if open_ports:
            self.result_box.append(f"发现以下打开的端口: {', '.join(map(str, open_ports))}")
        else:
            self.result_box.append("未发现打开的端口。")

    def display_error(self, error_message):
        """显示错误信息"""
        self.scan_button.setEnabled(True)
        self.progress_bar.hide()
        self.description_label.setText("好像遇到问题了...")
        self.result_box.append(f"错误: {error_message}")




if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner_app = PortScannerApp()
    scanner_app.show()
    sys.exit(app.exec())
