from PyQt5.QtWidgets import QWidget, QVBoxLayout, QProgressBar, QHBoxLayout, QLabel
from PyQt5.QtCore import pyqtSignal, QObject, Qt, QTimer
from PyQt5.QtGui import QColor, QPalette
from loguru import logger


class ProgressWidget(QWidget):
    def __init__(self, parent=None):
        """
        构造函数，初始化进度条工具类，创建并设置相关的部件和布局
        :param parent: 父部件，默认为 None，表示该部件没有父部件（顶级部件），可以根据实际需求传入相应的父部件
        """
        super().__init__(parent)

        # 创建用于承载进度条的窗口部件
        self.widget = QWidget()
        self.get_parent_size()
        self.widget.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.widget.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明

        # 创建布局
        layout = QVBoxLayout(self.widget)

        # 添加进度条描述标签
        self.label = QLabel("正在进行中...", self.widget)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("color: red; font-size: 16px;")
        layout.addWidget(self.label)

        # 创建进度条实例
        self.progress_bar = QProgressBar(self.widget)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(True)  # 显示进度条文本
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                background: #f2f2f2;
                height: 30px;
            }
            QProgressBar::chunk {
                background-color: #5cb85c;
                border-radius: 5px;
            }
        """)
        layout.addWidget(self.progress_bar)

        # 设置主布局
        self.layout = layout
        self.widget.setLayout(self.layout)

        # 定时更新进度条的文本
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress_text)

    def get_parent_size(self):
        """获取父窗口的大小并设置当前窗口的位置和大小"""
        parent = self.parent()
        if parent:
            # 获取主窗口的位置信息（x、y坐标）
            x = parent.x()
            y = parent.y()
            # 获取主窗口的大小信息（宽度和高度）
            width = parent.width()
            height = parent.height()
            logger.info(f"主窗口的位置：横坐标为{x}，纵坐标为{y}")
            logger.info(f"主窗口的大小：宽度为{width}，高度为{height}")
            self.widget.setGeometry(x, y, width, height)
        # parent = self.parent()
        # if parent:
        #     x = parent.x() + parent.width() // 4
        #     y = parent.y() + parent.height() // 4
        #     width = parent.width() // 2
        #     height = parent.height() // 10
        #     self.widget.setGeometry(x, y, width, height)

    def show(self):
        """显示包含进度条的窗口"""
        self.widget.show()

    def hide(self):
        """隐藏包含进度条的窗口"""
        self.widget.hide()

    def set_value(self, value):
        """设置进度条的值"""
        self.progress_bar.setValue(value)

    def set_range(self, min_value, max_value):
        """设置进度条的范围"""
        self.progress_bar.setRange(min_value, max_value)

    def set_format(self, format_str):
        """设置进度条显示的格式文本"""
        self.progress_bar.setFormat(format_str)

    def update_progress_text(self):
        """定期更新进度条上的文本"""
        progress = self.progress_bar.value()
        self.label.setText(f"进度：{progress}%")

    def connect_update_function(self, func):
        """连接外部的更新函数，当需要更新进度时调用该函数"""
        self.progress_bar.valueChanged.connect(func)


class ProgressSignalEmitter(QObject):
    progress_signal = pyqtSignal(int)
    """用于在有进度更新时发出信号的类，方便在不同任务中触发进度更新"""

    def update_progress(self, value):
        self.progress_signal.emit(value)

