import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout, QSpinBox, \
    QColorDialog, QSlider
from PySide6.QtCore import Qt, QPoint
from PySide6.QtGui import QMouseEvent, QGuiApplication, QColorConstants, QIcon
from loguru import logger

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.hover_image_button import HoverImageButton
from src.widget.sub_window_widget import SubWindowWidget


class DraggableLabel(QWidget):
    def __init__(self, text, parent=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self.draggable = False
        self.offset = None

        # 主布局
        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(5, 5, 5, 5)  # 设置边距

        # 文本标签
        self.text_label = QLabel(text)
        self.text_label.setStyleSheet("background-color: lightblue; padding: 5px; font-weight: bold;")
        self.layout.addWidget(self.text_label)

        # 关闭按钮
        self.close_button = QPushButton("×")  # 使用叉号作为关闭按钮
        self.close_button.setStyleSheet("background-color: red; color: white; font-weight: bold; border: none; min-width: 15px;")
        self.close_button.clicked.connect(self.close_label)  # 绑定点击事件
        self.layout.addWidget(self.close_button)

        # 设置窗口背景透明
        self.setStyleSheet("background-color: lightblue;")

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = True
            self.offset = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.draggable and event.buttons() & Qt.MouseButton.LeftButton:
            new_pos = self.mapToParent(event.position().toPoint() - self.offset)
            self.move(new_pos)

            # 更新透明窗口的位置，使其随着标签移动
            if hasattr(self, "transparent_window"):
                # 获取屏幕的大小
                screen_geometry = QGuiApplication.primaryScreen().geometry()
                screen_width = screen_geometry.width()
                screen_height = screen_geometry.height()

                mini_plane = self.parentWidget().geometry()
                mini_plane_width = mini_plane.width()
                mini_plane_height = mini_plane.height()

                # 计算 x 坐标的比例
                width_ratio = screen_width / mini_plane_width
                # 计算 y 坐标的比例
                height_ratio = screen_height / mini_plane_height
                # 计算透明窗口新的 x、y 坐标
                transparent_x = new_pos.x() * width_ratio
                transparent_y = new_pos.y() * height_ratio

                self.transparent_window.move(int(transparent_x), int(transparent_y))
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.draggable = False
        super().mouseReleaseEvent(event)

    def close_label(self):
        """关闭标签及其关联的透明窗口"""
        if hasattr(self, "transparent_window"):
            self.transparent_window.close()  # 关闭透明窗口
        self.close()  # 关闭标签


class TransparentWindow(QWidget):
    def __init__(self, text, color, font_size):
        super().__init__()
        # 设置窗口为无边框且置顶
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        # 设置窗口背景透明
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QVBoxLayout()
        # 创建用于显示文本的标签
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # 设置标签样式
        # 设置标签样式
        style = f"font-size: {font_size}px; font-weight: bold; color: {color.name()};"
        self.text_label.setStyleSheet(style)
        layout.addWidget(self.text_label)
        self.setLayout(layout)

        # 根据文本内容调整窗口大小
        self.adjustSize()


class CustomPanelApp(SubWindowWidget):
    def __init__(self):
        super().__init__()
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_CUSTOM_PANEL} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_CUSTOM_PANEL)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        # 创建布局
        layout = QVBoxLayout()

        # 创建桌面方框
        self.desktop = QWidget()
        self.desktop.setStyleSheet("background-color: lightgray;")
        self.desktop.setMinimumSize(600, 300)
        self.desktop.setMouseTracking(True)
        self.desktop.mouseMoveEvent = self.on_desktop_mouse_move
        layout.addWidget(self.desktop)

        # 创建输入框和添加按钮
        input_layout = QVBoxLayout()
        self.input_box = QLineEdit()
        input_layout.addWidget(self.input_box)

        # 颜色选择按钮
        self.color_button = QPushButton("选择颜色")
        self.color_button.clicked.connect(self.select_color)
        self.selected_color = QColorConstants.Black
        input_layout.addWidget(self.color_button)

        # 字体大小滑块
        self.font_size_slider = QSlider(Qt.Orientation.Horizontal)
        self.font_size_slider.setRange(14, 100)
        self.font_size_slider.setValue(24)
        self.label = QLabel(f"滑块当前值: {self.font_size_slider.value()}")
        self.font_size_slider.valueChanged.connect(self.on_slider_value_changed)

        input_layout.addWidget(self.label)
        input_layout.addWidget(self.font_size_slider)

        self.add_button = QPushButton("添加")
        self.add_button.clicked.connect(self.add_text_to_desktop)
        input_layout.addWidget(self.add_button)

        # 显示鼠标位置的标签
        self.mouse_pos_label = QLabel("鼠标位置: (0, 0)")
        input_layout.addWidget(self.mouse_pos_label)

        layout.addLayout(input_layout)

        # 设置布局
        self.setLayout(layout)

    def on_slider_value_changed(self, value):
        self.label.setText(f"滑块当前值: {value}")

    def select_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.selected_color = color

    def add_text_to_desktop(self):
        text = self.input_box.text()
        if text:
            label = DraggableLabel(text, self.desktop)
            label.move(50, 50)
            label.show()

            # 获取选择的颜色和字体大小
            color = self.selected_color
            font_size = self.font_size_slider.value()

            # 创建透明窗口并传入文本、颜色和字体大小
            transparent_window = TransparentWindow(text, color, font_size)
            # 设置透明窗口的位置为桌面区域的某个位置（例如左上角偏移50像素）
            transparent_window.move(50, 50)  # 透明窗口与标签有相同的初始位置
            transparent_window.show()

            # 将透明窗口与标签关联
            label.transparent_window = transparent_window
            self.input_box.clear()

    def on_desktop_mouse_move(self, event: QMouseEvent):
        pos = event.position().toPoint()
        self.mouse_pos_label.setText(f"鼠标位置: ({pos.x()}, {pos.y()})")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomPanelApp()
    window.show()
    sys.exit(app.exec())