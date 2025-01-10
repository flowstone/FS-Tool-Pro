import sys
import threading
import time
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget
from PySide6.QtGui import QCursor
import pyautogui


class MouseClicker(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("鼠标连点器")
        self.setFixedSize(300, 250)

        # 初始化状态
        self.clicking = False
        self.click_thread = None
        self.click_position = None  # 默认点击位置

        # 界面布局
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        # 提示标签
        self.label_interval = QLabel("设置点击间隔时间（秒）：")
        layout.addWidget(self.label_interval)

        # 输入框
        self.input_interval = QLineEdit()
        self.input_interval.setPlaceholderText("例如：0.1")
        self.input_interval.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.input_interval)

        # 设置位置按钮
        self.set_position_button = QPushButton("设置点击位置")
        self.set_position_button.clicked.connect(self.set_click_position)
        layout.addWidget(self.set_position_button)

        # 显示点击位置
        self.position_label = QLabel("点击位置：未设置")
        self.position_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.position_label)

        # 开始按钮
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_clicking)
        layout.addWidget(self.start_button)

        # 停止按钮
        self.stop_button = QPushButton("停止")
        self.stop_button.clicked.connect(self.stop_clicking)
        self.stop_button.setEnabled(False)
        layout.addWidget(self.stop_button)

        # 状态提示
        self.status_label = QLabel("状态：未开始")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)

        # 主窗口设置
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def set_click_position(self):
        # 获取当前鼠标的位置
        self.click_position = QCursor.pos()
        self.position_label.setText(f"点击位置：{self.click_position.x()}, {self.click_position.y()}")

    def start_clicking(self):
        if self.click_position is None:
            self.status_label.setText("状态：请先设置点击位置！")
            return

        try:
            interval = float(self.input_interval.text())
            if interval <= 0:
                raise ValueError
        except ValueError:
            self.status_label.setText("状态：间隔时间无效，请输入有效数字！")
            return

        self.clicking = True
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)
        self.status_label.setText("状态：连点中...")

        # 开启线程执行连点
        self.click_thread = threading.Thread(target=self.click_loop, args=(interval,))
        self.click_thread.start()

    def stop_clicking(self):
        self.clicking = False
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.status_label.setText("状态：已停止")

    def click_loop(self, interval):
        while self.clicking:
            # 使用设置的位置进行点击
            pyautogui.click(self.click_position.x(), self.click_position.y())
            time.sleep(interval)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 检测 pyautogui 模块是否正常运行
    try:
        QCursor.pos()
    except Exception as e:
        print(f"检测鼠标权限错误：{e}")
        sys.exit()

    window = MouseClicker()
    window.show()
    sys.exit(app.exec())
