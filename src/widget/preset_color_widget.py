import sys
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PySide6.QtGui import QColor
from PySide6.QtCore import Qt


class PresetColorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.last_clicked_button = None  # 记录上一次点击的按钮

        self.initUI()

    def initUI(self):
        # 预设颜色列表，添加了更多颜色
        preset_colors = [
            QColor(255, 0, 0),  # 红色
            QColor(0, 255, 0),  # 绿色
            QColor(0, 0, 255),  # 蓝色
            QColor(255, 255, 0),  # 黄色
            QColor(255, 0, 255),  # 紫色
            QColor(0, 255, 255),  # 青色
            QColor(128, 0, 0),  # 栗色
            QColor(0, 128, 0),  # 深绿色
            QColor(0, 0, 128),  # 深蓝色
            QColor(128, 128, 0),  # 橄榄色
            QColor(128, 0, 128),  # 深紫色
            QColor(255, 255, 255),  # 深青色
            QColor(255, 165, 0),  # 橙色
            QColor(255, 192, 203),  # 粉红色
            QColor(192, 192, 192),  # 银色
            QColor(128, 128, 128),  # 灰色
            QColor(240, 230, 140),  # 浅黄色
            QColor(210, 105, 30),  # 巧克力色
            QColor(0, 139, 139),  # 深青绿色
            QColor(139, 0, 139),  # 深紫红色
            QColor(0, 0, 0),  # 黑色
        ]

        # 创建主布局
        main_layout = QVBoxLayout()

        # 创建颜色信息标签
        self.color_info_label = QLabel("请选择一个颜色")
        main_layout.addWidget(self.color_info_label)

        # 用于存储每行的水平布局
        row_layout = QHBoxLayout()
        for i, color in enumerate(preset_colors):
            button = QPushButton()
            button.setStyleSheet(f"background-color: {color.name()}; width: 20px; height: 20px; border: 1px solid white;")
            button.clicked.connect(lambda _, c=color, btn=button: self.on_color_button_clicked(c, btn))
            row_layout.addWidget(button)

            # 每 7 个按钮换行
            if (i + 1) % 7 == 0:
                main_layout.addLayout(row_layout)
                row_layout = QHBoxLayout()

        # 如果最后一行不足 7 个按钮，也添加到主布局中
        if row_layout.count() > 0:
            main_layout.addLayout(row_layout)

        self.setLayout(main_layout)
        self.setWindowTitle("预设颜色组件")
        self.show()

    def on_color_button_clicked(self, color, button):
        # 显示颜色信息
        color_info = f"选中颜色: {color.name()}, RGB: ({color.red()}, {color.green()}, {color.blue()})"
        self.color_info_label.setText(color_info)

        # 恢复上一次点击按钮的样式
        if self.last_clicked_button:
            self.last_clicked_button.setStyleSheet(
                f"background-color: {self.last_clicked_button.palette().button().color().name()}; border: 1px solid white; width: 20px; height: 20px;")

        # 添加点击特效，这里添加一个白色边框
        button.setStyleSheet(
            f"background-color: {color.name()}; border: 1px solid black; width: 20px; height: 20px;")
        self.last_clicked_button = button


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PresetColorWidget()
    sys.exit(app.exec())