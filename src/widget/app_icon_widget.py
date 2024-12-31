# app_icon_widget.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsOpacityEffect, QGraphicsColorizeEffect
from PyQt5.QtCore import pyqtSignal, Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QPixmap, QColor


class AppIconWidget(QWidget):
    # 定义一个信号，当图标被点击时发出
    iconClicked = pyqtSignal(str)  # 传递图标名称

    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)

        # 保存名称和图标路径
        self.icon_path = icon_path
        self.name = name

        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(0)  # 去掉图标和名称之间的间距

        # 创建第一个 QLabel 用于显示图标
        self.icon_label = QLabel(self)
        pixmap = QPixmap(icon_path)  # 加载图片

        # 设置固定大小，确保图片自适应显示
        self.icon_label.setFixedSize(80, 80)  # 设置固定的图标显示大小
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)  # 图标居中显示
        self.icon_label.setScaledContents(True)  # 让图片按QLabel大小缩放

        # 创建第二个 QLabel 用于显示名称
        self.name_label = QLabel(name, self)
        self.name_label.setAlignment(Qt.AlignCenter)  # 名称居中显示
        self.name_label.setStyleSheet("font-size: 14px; color: #333;")  # 设置字体大小和颜色
        self.name_label.setMargin(0)  # 去除内边距，确保文字紧贴图标

        # 设置名称标签最大宽度为图片宽度
        self.name_label.setMaximumWidth(100)  # 设置最大宽度与图片一致

        # 将两个 QLabel 添加到布局中
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)

        # 设置布局
        self.setLayout(layout)

        # 设置鼠标样式
        self.setCursor(Qt.PointingHandCursor)  # 设置鼠标样式为手指图标

        # 设置固定大小
        self.setFixedSize(100, 120)  # 设置整个小部件的固定大小（宽度与图标相同，高度适合图标和名称）
        # 图标颜色特效
        self.color_effect = QGraphicsColorizeEffect(self.icon_label)
        self.color_effect.setColor(QColor("#1E90FF"))  # 设置染色颜色为蓝色

        self.icon_label.setGraphicsEffect(self.color_effect)

        # 创建颜色动画
        self.color_animation = QPropertyAnimation(self.color_effect, b"color")
        self.color_animation.setDuration(200)  # 动画时长 200 毫秒
        self.color_animation.setEasingCurve(QEasingCurve.InOutQuad)

    def mousePressEvent(self, event):
        """鼠标按下时改变颜色"""
        # 设置颜色动画：从白色变为深灰色
        self.color_animation.setStartValue(QColor("4169E1"))
        self.color_animation.setEndValue(QColor("#1E90FF"))
        self.color_animation.start()

        # 发出点击信号
        self.iconClicked.emit(self.name)

        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放时恢复颜色"""
        # 设置颜色动画：从灰色恢复为白色
        self.color_animation.setStartValue(QColor("#1E90FF"))
        self.color_animation.setEndValue(QColor("4169E1"))
        self.color_animation.start()

        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """鼠标悬停时颜色加深"""
        self.color_animation.setStartValue(QColor("#1E90FF"))
        self.color_animation.setEndValue(QColor("#6495ED"))
        self.color_animation.start()

        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时恢复原始颜色"""
        self.color_animation.setStartValue(QColor("#6495ED"))
        self.color_animation.setEndValue(QColor("#1E90FF"))
        self.color_animation.start()

        super().leaveEvent(event)