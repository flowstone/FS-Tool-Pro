import socket
import sys

import psutil
import requests
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QLabel
)
from loguru import logger

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.custom_progress_widget import CustomProgressBar


def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip


def get_local_ipv6():
    try:
        s = socket.socket(socket.AF_INET6, socket.SOCK_DGRAM)
        s.connect(('2001:4860:4860::8888', 80))
        local_ipv6 = s.getsockname()[0]
        s.close()
        return local_ipv6
    except Exception:
        return "未找到 IPv6 地址"


def get_mac_address():
    addrs = psutil.net_if_addrs()
    for interface_name, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == psutil.AF_LINK:
                return address.address
    return "无法获取 MAC 地址"


def get_gateway():
    gateways = psutil.net_if_addrs()
    for interface_name, interface_addresses in gateways.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET:
                if address.address == get_local_ip():
                    return address.broadcast
    return "未找到网关地址"


def get_external_ip():
    services = [
        "https://api.ipify.org?format=json",
        "http://icanhazip.com",
        "https://ident.me"
    ]
    for service in services:
        try:
            response = requests.get(service, timeout=5)
            if response.status_code == 200:
                if "api.ipify.org" in service:
                    return response.json().get("ip", "无法获取外网 IP")
                return response.text.strip()
        except requests.exceptions.RequestException:
            continue
    return "无法获取外网 IP"


def get_network_name():
    network_name = "未连接网络"
    ifaces = psutil.net_if_stats()
    for iface, stats in ifaces.items():
        if stats.isup:
            if "Wi-Fi" in iface or "wlan" in iface.lower():
                network_name = f"无线网络: {iface}"
            else:
                network_name = f"有线网络: {iface}"
            break
    return network_name


def check_internet_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return "已连接互联网"
    except OSError:
        return "未连接互联网"

def check_google_connectivity():
    """
    检测是否可以访问 Google
    :return: (bool, str) 如果成功，返回 (True, 响应时间)；否则返回 (False, 错误信息)
    """
    try:
        import time
        start_time = time.time()  # 开始计时
        response = requests.get("https://www.google.com", timeout=5)
        if response.status_code == 200:
            end_time = time.time()  # 结束计时
            elapsed_time = round((end_time - start_time) * 1000, 2)  # 响应时间（毫秒）
            return  f"成功访问 Google，响应时间: {elapsed_time} ms"
        else:
            return f"无法访问 Google，状态码: {response.status_code}"
    except requests.exceptions.RequestException as e:
        return  f"错误: {str(e)}"

def get_dns_servers_windows():
    import winreg
    dns_servers = []
    try:
        with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Services\Tcpip\Parameters") as key:
            value, _ = winreg.QueryValueEx(key, "NameServer")
            dns_servers = value.split(",")
    except Exception:
        pass
    return dns_servers


def get_dns_servers():
    if CommonUtil.check_win_os():
        return get_dns_servers_windows()
    else:
        import subprocess
        if hasattr(subprocess, 'check_output'):
            try:
                output = subprocess.check_output(['cat', '/etc/resolv.conf']).decode()
                dns_servers = []
                for line in output.splitlines():
                    if line.startswith('nameserver'):
                        dns_server = line.split()[1]
                        dns_servers.append(dns_server)
                return dns_servers
            except Exception:
                pass
    return ["N/A"]

class NetworkInfoWorker(QThread):
    # 定义信号，用于传递网络信息和进度
    progress_signal = pyqtSignal(int)
    result_signal = pyqtSignal(str)
    error_signal = pyqtSignal(str)    # 错误信号

    def run(self):
        try:

            info = ""
            steps = [
                ("网络名称", get_network_name),
                ("网络状态", check_internet_connection),
                ("本地 IPv4 地址", get_local_ip),
                ("本地 IPv6 地址", get_local_ipv6),
                ("本地 MAC 地址", get_mac_address),
                ("网关地址", get_gateway),
                ("外网 IP 地址", get_external_ip),
                ("DNS 地址", get_dns_servers),
            ]
            total_steps = len(steps)

            for i, (desc, func) in enumerate(steps):
                result = func()
                info += f"{desc}: {result}\n"
                self.progress_signal.emit(int((i + 1) / total_steps * 100))  # 更新进度
            self.result_signal.emit(info)  # 发送结果信号
        except Exception as e:
            self.error_signal.emit(str(e))  # 发送错误信号

class IpInfoApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IP_INFO} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_IP_INFO)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setGeometry(100, 100, 500, 400)

        title_label = QLabel(FsConstants.WINDOW_TITLE_IP_INFO)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        self.button = QPushButton("获取网络信息")
        self.button.clicked.connect(self.fetch_network_info)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.text_area)
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def fetch_network_info(self):
        """
        启动多线程获取网络信息
        """
        self.text_area.clear()
        self.button.setEnabled(False)

        self.worker = NetworkInfoWorker()
        self.worker.progress_signal.connect(self.progress_bar.update_progress)
        self.worker.result_signal.connect(self.display_result)
        self.worker.error_signal.connect(self.display_error)  # 连接错误信号
        self.worker.start()
        self.progress_bar.show()


    def display_result(self, result):
        """
        显示网络信息并重置按钮状态
        """
        self.progress_bar.hide()
        self.text_area.setText(result)
        self.button.setEnabled(True)
    def display_error(self, error):
        """
        显示错误信息并重置按钮状态
        """
        self.progress_bar.hide()

        self.text_area.setText(f"发生错误：\n{error}")
        self.button.setEnabled(True)

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IpInfoApp()
    window.show()
    sys.exit(app.exec_())
