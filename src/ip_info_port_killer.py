import socket
import socket
import sys
from concurrent.futures import ThreadPoolExecutor

import psutil
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QPushButton, QListWidget, QLabel, QLineEdit, QHBoxLayout
)

from src.const.color_constants import BLACK, BLUE
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.message_util import MessageUtil
from src.util.permission_util import check_admin
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
class PortScannerThread(QThread):
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
        self.result_signal.emit(open_ports)

class PortKillerApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle(FsConstants.PORT_KILLER_WINDOW_TITLE)
        #self.setGeometry(100, 100, 600, 500)
        self.setFixedWidth(600)
        self.initUI()

    def initUI(self):
        # 主界面布局
        self.layout = QVBoxLayout(self)

        title_label = QLabel(FsConstants.PORT_KILLER_WINDOW_TITLE)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        self.layout.addWidget(title_label)
        # 标题
        self.description_label = QLabel("输入目标 IP 和端口范围，点击搜索按钮查看被占用的端口")
        self.description_label.setStyleSheet(f"color: {BLUE.name()};")

        # 输入目标 IP
        self.ip_input_label = QLabel("目标 IP 地址:")
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("例如: 127.0.0.1")
        self.ip_input.setText("127.0.0.1")

        # 输入端口范围
        self.port_input_label = QLabel("端口范围 (起始-结束):")
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("例如: 1-1000")
        self.port_input.setText("1-65535")

        # 进度条
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        button_layout = QHBoxLayout()
        # 搜索按钮
        self.search_button = QPushButton("搜索")
        self.search_button.clicked.connect(self.search_ports)
        # 停止按钮
        self.kill_button = QPushButton("停止")
        self.kill_button.clicked.connect(self.kill_port)
        button_layout.addWidget(self.search_button)
        button_layout.addWidget(self.kill_button)
        # 显示端口列表
        self.port_list = QListWidget()


        # 添加到布局
        self.layout.addWidget(self.description_label)
        self.layout.addWidget(self.ip_input_label)
        self.layout.addWidget(self.ip_input)
        self.layout.addWidget(self.port_input_label)
        self.layout.addWidget(self.port_input)
        self.layout.addLayout(button_layout)
        self.layout.addWidget(self.progress_bar)
        self.layout.addWidget(self.port_list)

    def search_ports(self):
        """搜索被占用的端口"""
        self.port_list.clear()
        self.progress_bar.setValue(0)
        target_ip = self.ip_input.text().strip()
        port_range = self.port_input.text().strip()

        try:
            start_port, end_port = map(int, port_range.split("-"))
            if start_port < 1 or end_port > 65535 or start_port > end_port:
                raise ValueError
        except ValueError:
            MessageUtil.show_warning_message("端口范围格式不正确，请输入有效范围 (例如: 1-1000)！")
            return

        self.description_label.setText("正在扫描端口，请稍候...")
        self.search_button.setEnabled(False)
        # 启动后台线程
        self.scanner_thread = PortScannerThread(target_ip, start_port, end_port)
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

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

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
            check_admin()
            for conn in psutil.net_connections(kind="inet"):
                if conn.laddr and conn.laddr.port == port:
                    pid = conn.pid
                    if pid:
                        psutil.Process(pid).terminate()
                        MessageUtil.show_success_message(f"端口 {port} 已被成功释放！")
                        self.search_ports()  # 刷新端口列表
                        return

        except psutil.AccessDenied:
            MessageUtil.show_error_message("操作被拒绝！请以管理员身份运行程序。")
            return
        except Exception as e:
            MessageUtil.show_error_message(f"无法终止进程：{str(e)}")
            return
        MessageUtil.show_warning_message(f"未能找到占用端口 {port} 的进程。")


if __name__ == "__main__":
    # 创建 QApplication 实例
    app = QApplication(sys.argv)
    killer_app = PortKillerApp()
    killer_app.show()
    sys.exit(app.exec_())
