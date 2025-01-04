import sys
import time

from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QGuiApplication
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QDialog, QComboBox, QHBoxLayout
from loguru import logger

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil


class DesktopClockApp(QWidget):

    def __init__(self):
        super().__init__()
        self.elapsed_time = 0
        self.init_ui()
        self.selected_time_color = "white"
        self.selected_timer_color = "pink"

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_DESKTOP_CLOCK} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_DESKTOP_CLOCK)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 设置窗口无边框、无标题栏
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)  # 设置窗口背景透明
        # 设置窗口透明度
        self.setWindowOpacity(0.8)

        self.setGeometry(0, 0, 200, 80)

        layout = QVBoxLayout()

        self.current_time = QLabel(self)
        self.current_time.setObjectName("current_time")
        self.current_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_time)

        self.count_time = QLabel(self)
        self.count_time.setObjectName("count_time")
        self.count_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.count_time)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        self.setLayout(layout)

    def show_with_colors(self, time_color, timer_color):
        self.selected_time_color = time_color
        self.selected_timer_color = timer_color
        self.update_colors()
        self.timer.start(1000)
        self.show()

    def update_colors(self):
        """
         根据所选颜色更新时间显示文本的颜色
        """
        color_css = {
            "白色": "white",
            "粉色": "pink",
            "红色": "red",
            "绿色": "green",
            "蓝色": "blue"
        }
        self.current_time.setStyleSheet(f"color: {color_css[self.selected_time_color]};")
        self.count_time.setStyleSheet(f"color: {color_css[self.selected_timer_color]};")

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.current_time.setText(current_time)
        # 计时器
        self.elapsed_time += 1
        hours = self.elapsed_time // 3600
        minutes = (self.elapsed_time % 3600) // 60
        seconds = self.elapsed_time % 60
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        self.count_time.setText(time_str)

    def move_to_position(self, position):
        screen_geo = QGuiApplication.primaryScreen().geometry()
        x, y = 10, 10
        if position == "左上角":
            x, y = 10, 10
        elif position == "右上角":
            x, y = screen_geo.width() - self.width() - 100, 10
        elif position == "左下角":
            x, y = 10, screen_geo.height() - self.height() - 10
        elif position == "右下角":
            x, y = screen_geo.width() - self.width() - 100, screen_geo.height() - self.height() - 10

        self.move(x, y)

class DesktopClockSetting(QDialog):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("颜色设置")
        self.setFixedSize(250, 200)  # 设置固定大小，让界面更规整
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()



        # 创建时间选择行，使用QHBoxLayout使其占满宽度
        time_row_layout = QHBoxLayout()
        time_label = QLabel("时间")
        self.time_color_combobox = QComboBox(self)
        self.time_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])

        # 让时间选择的QComboBox占满剩余空间
        time_row_layout.addWidget(time_label)
        time_row_layout.addWidget(self.time_color_combobox)
        layout.addLayout(time_row_layout)



        # 创建计时器选择行，使用QHBoxLayout使其占满宽度
        timer_row_layout = QHBoxLayout()
        timer_label = QLabel("计时器")
        self.timer_color_combobox = QComboBox(self)
        self.timer_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])

        # 让计时器选择的QComboBox占满剩余空间
        timer_row_layout.addWidget(timer_label)
        timer_row_layout.addWidget(self.timer_color_combobox)
        layout.addLayout(timer_row_layout)

        # 创建窗口位置选择行
        position_row_layout = QHBoxLayout()
        position_label = QLabel("窗口位置")
        self.position_combobox = QComboBox(self)
        self.position_combobox.addItems(["左上角", "右上角", "左下角", "右下角"])
        position_row_layout.addWidget(position_label)
        position_row_layout.addWidget(self.position_combobox)
        layout.addLayout(position_row_layout)

        # 确定按钮
        ok_button = QPushButton("确定")
        ok_button.clicked.connect(self.start_operation)
        layout.addWidget(ok_button)

        self.setLayout(layout)
    def get_selected_time_color(self):
        return self.time_color_combobox.currentText()

    def get_selected_timer_color(self):
        return self.timer_color_combobox.currentText()

    def get_selected_position(self):
        return self.position_combobox.currentText()

    def start_operation(self):
        time_color = self.get_selected_time_color()
        timer_color = self.get_selected_timer_color()
        position = self.get_selected_position()

        self.window = DesktopClockApp()
        self.window.show_with_colors(time_color, timer_color)
        self.window.move_to_position(position)  # 移动窗口到所选位置
        self.hide()


    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    setting_dialog = DesktopClockSetting()
    setting_dialog.show()
    # if setting_dialog.exec():
    #     time_color = setting_dialog.get_selected_time_color()
    #     timer_color = setting_dialog.get_selected_timer_color()
    #
    #     window = DesktopClockApp()
    #     window.show_with_colors(time_color, timer_color)

    sys.exit(app.exec())