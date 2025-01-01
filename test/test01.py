import sys
import psutil
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal


def get_open_ports():
    """
    获取当前设备的所有网络端口信息
    """
    connections = psutil.net_connections(kind="inet")
    ports_info = []

    for conn in connections:
        laddr = conn.laddr.port if conn.laddr else "N/A"
        raddr = conn.raddr.port if conn.raddr else "N/A"
        status = conn.status
        ports_info.append(f"本地端口: {laddr} | 远程端口: {raddr} | 状态: {status}")

    if not ports_info:
        return ["未检测到任何打开的端口"]
    return ports_info


class PortScannerWorker(QThread):
    result_signal = pyqtSignal(list)  # 信号，用于返回结果

    def run(self):
        ports_info = get_open_ports()
        self.result_signal.emit(ports_info)  # 发送结果


class PortViewerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("本地端口查看器")
        self.setGeometry(100, 100, 600, 400)

        # 界面组件
        self.label = QLabel("点击按钮查看本地端口：")
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.button = QPushButton("刷新端口信息")
        self.button.clicked.connect(self.fetch_ports)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def fetch_ports(self):
        """
        开始获取端口信息
        """
        self.text_area.clear()
        self.button.setEnabled(False)

        # 启动后台线程获取端口
        self.worker = PortScannerWorker()
        self.worker.result_signal.connect(self.display_ports)
        self.worker.start()

    def display_ports(self, ports_info):
        """
        显示端口信息
        """
        self.text_area.setText("\n".join(ports_info))
        self.button.setEnabled(True)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortViewerApp()
    window.show()
    sys.exit(app.exec_())
