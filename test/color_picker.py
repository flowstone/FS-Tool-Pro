import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QVBoxLayout, QColorDialog
from PyQt5.QtGui import QColor, QPalette

class ColorPaletteApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("颜色板")
        self.setGeometry(400, 200, 300, 200)

        # 创建主布局
        layout = QVBoxLayout()

        # 颜色显示区域
        self.color_display = QLabel("当前颜色")
        self.color_display.setAlignment(Qt.AlignCenter)
        self.color_display.setFixedSize(200, 100)
        self.color_display.setStyleSheet("border: 1px solid black; background-color: white;")

        # 按钮：打开颜色选择器
        self.select_color_button = QPushButton("选择颜色")
        self.select_color_button.clicked.connect(self.open_color_picker)

        # 将控件添加到布局中
        layout.addWidget(self.color_display)
        layout.addWidget(self.select_color_button)

        self.setLayout(layout)

    def open_color_picker(self):
        # 打开颜色选择器
        color = QColorDialog.getColor()

        # 如果用户选择了有效颜色
        if color.isValid():
            # 更新颜色显示区域的背景色
            self.update_color_display(color)

    def update_color_display(self, color: QColor):
        """更新颜色显示区域的背景颜色"""
        self.color_display.setStyleSheet(f"border: 1px solid black; background-color: {color.name()};")
        self.color_display.setText(f"选中的颜色: {color.name()}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPaletteApp()
    window.show()
    sys.exit(app.exec_())
