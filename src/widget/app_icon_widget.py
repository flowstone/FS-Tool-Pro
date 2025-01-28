from PySide6.QtCore import Signal, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QPixmap, QColor
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QGraphicsColorizeEffect
from fs_base.config_manager import ConfigManager

from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants


class AppIconWidget(QWidget):
    # 定义一个信号，当图标被点击时发出
    iconClicked = Signal(str)  # 传递图标名称

    # 颜色字典，减少硬编码
    COLOR_NORMAL = QColor("#1E90FF")
    COLOR_PRESSED = QColor("4169E1")
    COLOR_HOVER = QColor("#6495ED")

    def __init__(self, icon_path, name, parent=None):
        super().__init__(parent)

        # 保存名称和图标路径
        self.icon_path = icon_path
        self.name = name
        self.config_manager = ConfigManager()
        self.config_manager.config_updated.connect(self.on_config_updated)
        self.icon_font_bold_checked = self.config_manager.get_config(FsConstants.APP_ICON_FONT_BOLD_CHECKED_KEY)
        # 创建布局
        layout = QVBoxLayout()
        layout.setSpacing(0)  # 去掉图标和名称之间的间距

        # 创建第一个 QLabel 用于显示图标
        self.icon_label = QLabel(self)
        pixmap = QPixmap(icon_path)  # 加载图片

        # 设置固定大小，确保图片自适应显示
        self.icon_label.setFixedSize(80, 80)  # 设置固定的图标显示大小
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 图标居中显示
        self.icon_label.setScaledContents(True)  # 让图片按QLabel大小缩放

        # 创建第二个 QLabel 用于显示名称
        self.name_label = QLabel(name, self)
        self.name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # 名称居中显示
        self.name_label.setMaximumWidth(100)  # 设置最大宽度与图片一致
        if self.icon_font_bold_checked:
            self.name_label.setFont(FontConstants.BOLD_SMALL)

        # 将两个 QLabel 添加到布局中
        layout.addWidget(self.icon_label)
        layout.addWidget(self.name_label)

        # 设置布局
        self.setLayout(layout)

        # 设置鼠标样式
        self.setCursor(Qt.CursorShape.PointingHandCursor)  # 设置鼠标样式为手指图标

        # 设置固定大小
        self.setFixedSize(100, 120)  # 设置整个小部件的固定大小（宽度与图标相同，高度适合图标和名称）

        # 图标颜色特效
        self.color_effect = QGraphicsColorizeEffect(self.icon_label)
        self.color_effect.setColor(self.COLOR_NORMAL)  # 初始颜色

        self.icon_label.setGraphicsEffect(self.color_effect)

        # 创建颜色动画
        self.color_animation = QPropertyAnimation(self.color_effect, b"color")
        self.color_animation.setDuration(200)  # 动画时长 200 毫秒
        self.color_animation.setEasingCurve(QEasingCurve.Type.InOutQuad)

    def _animate_color(self, start_color, end_color):
        """简化动画的颜色设置"""
        self.color_animation.setStartValue(start_color)
        self.color_animation.setEndValue(end_color)
        self.color_animation.start()

    def mousePressEvent(self, event):
        """鼠标按下时改变颜色"""
        self._animate_color(self.COLOR_PRESSED, self.COLOR_NORMAL)
        self.iconClicked.emit(self.name)  # 发出点击信号
        super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        """鼠标释放时恢复颜色"""
        self._animate_color(self.COLOR_NORMAL, self.COLOR_PRESSED)
        super().mouseReleaseEvent(event)

    def enterEvent(self, event):
        """鼠标悬停时颜色加深"""
        self._animate_color(self.COLOR_NORMAL, self.COLOR_HOVER)
        super().enterEvent(event)

    def leaveEvent(self, event):
        """鼠标离开时恢复原始颜色"""
        self._animate_color(self.COLOR_HOVER, self.COLOR_NORMAL)
        super().leaveEvent(event)

    def on_config_updated(self, key, value):
        if key == FsConstants.APP_ICON_FONT_BOLD_CHECKED_KEY:
            self.icon_font_bold_checked = self.config_manager.get_config(FsConstants.APP_ICON_FONT_BOLD_CHECKED_KEY)
            self.name_label.setFont(FontConstants.BOLD_SMALL if self.icon_font_bold_checked else FontConstants.BODY_SMALL)
