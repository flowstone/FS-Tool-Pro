import socket
import sys
from concurrent.futures import ThreadPoolExecutor

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QTextEdit, QLabel, QLineEdit
)

from src.const.color_constants import BLACK, BLUE
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.widget.custom_progress_widget import CustomProgressBar


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
        print(f"Error scanning port {port}: {e}")  # 打印错误信息
        return None

def get_open_ports(target_ip, start_port, end_port, progress_callback, error_callback):
    """
    扫描指定 IP 的端口范围，使用线程池并发
    """
    open_ports = []
    total_ports = end_port - start_port + 1
    progress = 0

    try:
        with ThreadPoolExecutor(max_workers=50) as executor:  # 设置线程池大小
            futures = [
                executor.submit(scan_port, target_ip, port)
                for port in range(start_port, end_port + 1)
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
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(list)
    error_signal = pyqtSignal(str)

    def __init__(self, target_ip, start_port, end_port):
        super().__init__()
        self.target_ip = target_ip
        self.start_port = start_port
        self.end_port = end_port

    def run(self):

        open_ports = get_open_ports(
            self.target_ip, self.start_port, self.end_port, self.progress_signal, self.error_signal
        )
        if open_ports is not None:
            self.result_signal.emit(open_ports)

class PortScannerApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(FsConstants.PORT_SCANNER_WINDOW_TITLE)
        self.setGeometry(100, 100, 600, 500)
        self.initUI()

    def initUI(self):
        # 主界面布局

        # 主界面布局
        self.layout = QVBoxLayout(self)
        title_label = QLabel(FsConstants.PORT_SCANNER_WINDOW_TITLE)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        self.layout.addWidget(title_label)
        # 标题
        self.description_label = QLabel("输入目标 IP 和端口范围，点击按钮开始扫描")
        self.description_label.setStyleSheet(f"color: {BLUE.name()};")

        # 输入目标 IP
        self.ip_input_label = QLabel("目标 IP 地址:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("例如: 192.168.1.1")
        self.ip_input.setText("127.0.0.1")
        # 输入端口范围
        self.port_input_label = QLabel("端口范围 (起始-结束):")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 1-65535")
        self.port_input.setText("1-65535")  # 设置默认值

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
        self.layout.addWidget(self.port_input_label)
        self.layout.addWidget(self.port_input)
        self.layout.addWidget(self.scan_button)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.result_box)

    def scan_ports(self):
        self.result_box.clear()
        self.progress_bar.setValue(0)  # 重置进度条

        target_ip = self.ip_input.text().strip()
        port_range = self.port_input.text().strip()

        # 检查输入是否合法
        if not target_ip:
            self.result_box.append("错误: 请输入目标 IP 地址！")
            return

        if not port_range:
            self.result_box.append("错误: 请输入端口范围！")
            return

        try:
            start_port, end_port = map(int, port_range.split("-"))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
        except ValueError:
            self.result_box.append("错误: 端口范围格式不正确，请输入有效范围 (例如: 1-1000)！")
            return

        self.result_box.append(f"正在扫描目标 IP: {target_ip}, 端口范围: {start_port}-{end_port}...")
        self.result_box.append("这可能需要一些时间，请耐心等待。")
        self.scan_button.setEnabled(False)
        # 启动扫描线程
        self.worker_thread = WorkerThread(target_ip, start_port, end_port)
        self.worker_thread.progress_signal.connect(self.progress_bar.update_progress)
        self.worker_thread.result_signal.connect(self.display_results)
        self.worker_thread.error_signal.connect(self.display_error)
        self.worker_thread.start()
        self.progress_bar.show()


    def display_results(self, open_ports):
        """显示扫描结果"""
        self.scan_button.setEnabled(True)
        self.progress_bar.hide()
        if open_ports:
            self.result_box.append(f"发现以下打开的端口: {', '.join(map(str, open_ports))}")
        else:
            self.result_box.append("未发现打开的端口。")

    def display_error(self, error_message):
        """显示错误信息"""
        self.scan_button.setEnabled(True)
        self.progress_bar.hide()
        self.result_box.append(f"错误: {error_message}")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    scanner_app = PortScannerApp()
    scanner_app.show()
    sys.exit(app.exec_())
