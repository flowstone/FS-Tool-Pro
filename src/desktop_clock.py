import sys
import time
from PySide6.QtCore import Qt, QTimer, Signal
from PySide6.QtGui import QGuiApplication, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QDialog, \
    QComboBox, QSpinBox, QGroupBox
from fs_base.widget import TransparentTextBox

from src.util.common_util import CommonUtil


class DesktopClockApp(QWidget):
    def __init__(self):
        super().__init__()
        self.elapsed_time = 0
        self.remaining_time = 0  # 倒计时初始剩余时间（秒）
        self.init_ui()
        self.selected_time_color = "white"
        self.selected_timer_color = "pink"
        self.selected_countdown_color = "blue"
        self.show_time = True
        self.show_timer = True
        self.show_countdown = True

    def init_ui(self):
        self.setWindowTitle("桌面时钟")
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint | Qt.WindowType.Tool)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground, True)  # 设置窗口背景透明

        self.setWindowOpacity(0.8)
        self.setGeometry(0, 0, 200, 120)

        layout = QVBoxLayout()

        # 当前时间显示
        self.current_time = QLabel(self)
        self.current_time.setObjectName("current_time")
        self.current_time.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.current_time)

        # 计时器显示
        self.count_time = QLabel(self)
        self.count_time.setObjectName("count_time")
        self.count_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.count_time)

        # 倒计时显示
        self.countdown_time = QLabel(self)
        self.countdown_time.setObjectName("countdown_time")
        self.countdown_time.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignBottom)
        layout.addWidget(self.countdown_time)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_time)

        layout.addWidget(TransparentTextBox())

        self.setLayout(layout)

    def show_with_settings(self, time_color, timer_color, countdown_color, show_time, show_timer, show_countdown, countdown_duration):
        self.selected_time_color = time_color
        self.selected_timer_color = timer_color
        self.selected_countdown_color = countdown_color
        self.show_time = show_time
        self.show_timer = show_timer
        self.show_countdown = show_countdown
        self.remaining_time = countdown_duration  # 设置倒计时初始值
        self.update_colors()
        self.update_visibility()
        self.timer.start(1000)
        self.show()

    def update_colors(self):
        color_css = {
            "白色": "white",
            "粉色": "pink",
            "红色": "red",
            "绿色": "green",
            "蓝色": "blue"
        }
        self.current_time.setStyleSheet(f"color: {color_css[self.selected_time_color]};")
        self.count_time.setStyleSheet(f"color: {color_css[self.selected_timer_color]};")
        self.countdown_time.setStyleSheet(f"color: {color_css[self.selected_countdown_color]};")

    def update_visibility(self):
        """根据设置显示或隐藏时间、计时器和倒计时"""
        self.current_time.setVisible(self.show_time)
        self.count_time.setVisible(self.show_timer)
        self.countdown_time.setVisible(self.show_countdown)

    def update_time(self):
        current_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        self.current_time.setText(current_time)

        # 更新计时器
        if self.show_timer:
            self.elapsed_time += 1
            hours = self.elapsed_time // 3600
            minutes = (self.elapsed_time % 3600) // 60
            seconds = self.elapsed_time % 60
            self.count_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")

        # 更新倒计时
        if self.show_countdown and self.remaining_time > 0:
            self.remaining_time -= 1
            hours = self.remaining_time // 3600
            minutes = (self.remaining_time % 3600) // 60
            seconds = self.remaining_time % 60
            self.countdown_time.setText(f"{hours:02d}:{minutes:02d}:{seconds:02d}")
        elif self.show_countdown and self.remaining_time == 0:
            self.countdown_time.setText("时间到！")


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
    closed_signal = Signal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("设置")
        self.setFixedWidth(400)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()

        # 时间显示开关
        time_group_layout = QVBoxLayout()
        time_group = QGroupBox("时间")

        time_row_layout = QHBoxLayout()
        self.time_checkbox = QCheckBox("显示时间")
        self.time_checkbox.setChecked(True)
        time_group_layout.addWidget(self.time_checkbox)

        # 时间颜色选择
        time_label = QLabel("颜色")
        self.time_color_combobox = QComboBox(self)
        self.time_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])
        time_row_layout.addWidget(time_label)
        time_row_layout.addWidget(self.time_color_combobox)
        time_group_layout.addLayout(time_row_layout)
        time_group.setLayout(time_group_layout)
        layout.addWidget(time_group)

        # 计时器显示开关
        timer_group_layout = QVBoxLayout()
        timer_group = QGroupBox("计时器")
        timer_row_layout = QHBoxLayout()
        self.timer_checkbox = QCheckBox("显示计时器")
        timer_group_layout.addWidget(self.timer_checkbox)

        # 计时器颜色选择
        timer_label = QLabel("颜色")
        self.timer_color_combobox = QComboBox(self)
        self.timer_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])
        timer_row_layout.addWidget(timer_label)
        timer_row_layout.addWidget(self.timer_color_combobox)
        timer_group_layout.addLayout(timer_row_layout)
        timer_group.setLayout(timer_group_layout)
        layout.addWidget(timer_group)

        # 倒计时显示开关
        countdown_group_layout = QVBoxLayout()
        countdown_group = QGroupBox("倒计时")
        countdown_row_layout = QHBoxLayout()
        self.countdown_checkbox = QCheckBox("显示倒计时")
        countdown_group_layout.addWidget(self.countdown_checkbox)

        # 倒计时颜色选择
        countdown_label = QLabel("颜色")
        self.countdown_color_combobox = QComboBox(self)
        self.countdown_color_combobox.addItems(["白色", "粉色", "红色", "绿色", "蓝色"])
        countdown_row_layout.addWidget(countdown_label)
        countdown_row_layout.addWidget(self.countdown_color_combobox)

        # 倒计时时长输入
        # 倒计时时长输入（小时、分钟、秒）
        duration_layout = QHBoxLayout()
        duration_label = QLabel("倒计时时长")
        self.hours_spinbox = QSpinBox(self)
        self.hours_spinbox.setRange(0, 23)
        self.hours_spinbox.setSuffix(" 小时")
        self.minutes_spinbox = QSpinBox(self)
        self.minutes_spinbox.setRange(0, 59)
        self.minutes_spinbox.setSuffix(" 分钟")
        self.seconds_spinbox = QSpinBox(self)
        self.seconds_spinbox.setRange(0, 59)
        self.seconds_spinbox.setSuffix(" 秒")
        duration_layout.addWidget(duration_label)
        duration_layout.addWidget(self.hours_spinbox)
        duration_layout.addWidget(self.minutes_spinbox)
        duration_layout.addWidget(self.seconds_spinbox)
        countdown_group_layout.addLayout(countdown_row_layout)
        countdown_group_layout.addLayout(duration_layout)
        countdown_group.setLayout(countdown_group_layout)
        layout.addWidget(countdown_group)

        # 窗口位置选择
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

    def start_operation(self):
        time_color = self.time_color_combobox.currentText()
        timer_color = self.timer_color_combobox.currentText()
        countdown_color = self.countdown_color_combobox.currentText()
        show_time = self.time_checkbox.isChecked()
        show_timer = self.timer_checkbox.isChecked()
        show_countdown = self.countdown_checkbox.isChecked()
        position = self.position_combobox.currentText()
        # 获取倒计时时长（小时、分钟、秒）
        countdown_duration = (
                self.hours_spinbox.value() * 3600 +
                self.minutes_spinbox.value() * 60 +
                self.seconds_spinbox.value()
        )
        # 启动桌面时钟应用
        self.clock_app = DesktopClockApp()
        self.clock_app.show_with_settings(time_color, timer_color, countdown_color, show_time, show_timer, show_countdown, countdown_duration)
        self.clock_app.move_to_position(position)
        self.close()


def main():
    app = QApplication(sys.argv)
    settings = DesktopClockSetting()
    settings.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
