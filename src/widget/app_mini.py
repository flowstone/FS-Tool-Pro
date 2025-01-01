from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer, QEasingCurve
from PyQt5.QtGui import QMouseEvent, QPixmap
from loguru import logger
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from PyQt5.QtCore import QPropertyAnimation, QPoint
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsEllipseItem
from PyQt5.QtCore import QTimer, QPointF
from PyQt5.QtGui import QColor
import random

class FloatingBall(QWidget):

    def __init__(self, main_window):
        super().__init__()
        # 清除外部QSS影响
        self.setStyleSheet("background-color: transparent;")
        self.main_window = main_window
        self.init_ui()



    def init_ui(self):
        logger.info("---- 悬浮球初始化 ----")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)

        self.setGeometry(0, 0, FsConstants.APP_MINI_WINDOW_WIDTH, FsConstants.APP_MINI_WINDOW_HEIGHT)  # 设置悬浮球大小
        self.setAttribute(Qt.WA_TranslucentBackground, True)  # 设置窗口背景透明

        #self.setWindowOpacity(0.8)  # 设置透明度

        self.setup_background_image()
        self.move_to_top_right()

        self.dragPosition = None
        self.setMouseTracking(True)



        # 启动呼吸灯效果（透明度周期性变化）
        #self.breathing_light_window()
        # 悬浮球的缓慢漂浮（上下浮动）
        self.add_float_animation()
        # 随机跑
        #self.add_random_walk()

    # 启动呼吸灯效果（透明度周期性变化）
    def breathing_light_window(self):
        logger.info("---- 悬浮球启动呼吸灯效果 ----")
        # 初始透明度
        self.opacity = 0.2
        # 透明度每次变化的值，控制呼吸的速度和节奏
        self.direction = 0.02
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_opacity)
        # 设置定时器间隔为50毫秒，可根据需要调整呼吸节奏快慢
        self.timer.start(50)


    def add_float_animation(self):
        # 创建属性动画，调整窗口位置
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(2000)  # 动画时长2秒
        self.animation.setStartValue(self.pos())  # 初始位置
        self.animation.setKeyValueAt(0.5, self.pos() + QPoint(0, 10))  # 浮动到10像素下方
        self.animation.setEndValue(self.pos())  # 回到原位置
        self.animation.setLoopCount(-1)  # 无限循环
        self.animation.setEasingCurve(QEasingCurve.InOutSine)  # 平滑效果
        self.animation.start()

    def update_animation_start_position(self):
        if hasattr(self, "animation"):
            # 停止当前动画
            self.animation.stop()

            # 更新动画起始位置为当前窗口位置
            self.animation.setStartValue(self.pos())

            # 更新动画结束位置（基于当前窗口位置计算浮动范围）
            self.animation.setKeyValueAt(0.5, self.pos() + QPoint(0, 10))  # 下浮10像素
            self.animation.setEndValue(self.pos())  # 回到原位置
            self.animation.start()

    def add_random_walk(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.random_move)
        self.timer.start(1000)  # 每秒移动一次

    def random_move(self):
        screen_geo = QApplication.desktop().screenGeometry()
        new_x = random.randint(0, screen_geo.width() - self.width())
        new_y = random.randint(0, screen_geo.height() - self.height())
        self.move(new_x, new_y)

    # 更新透明度
    def update_opacity(self):
        self.opacity += self.direction
        if self.opacity >= 1.0:
            self.direction = -0.02  # 达到最大透明度后开始减小透明度
        elif self.opacity <= 0.2:
            self.direction = 0.02  # 达到最小透明度后开始增大透明度
        self.setWindowOpacity(self.opacity)



    def setup_background_image(self):
        logger.info("---- 初始化悬浮球背景图 ----")

        layout = QVBoxLayout()
        # 这里使用一个示例图片路径，你可以替换为真实路径
        pixmap = QPixmap(CommonUtil.get_mini_ico_full_path())
        pixmap = pixmap.scaled(self.size())
        self.background_label = QLabel(self)
        self.background_label.setPixmap(pixmap)
        self.background_label.resize(self.size())
        layout.addWidget(self.background_label)
        self.setLayout(layout)


    def move_to_top_right(self):
        logger.info("---- 初始化悬浮球位置 ----")
        screen_geo = QApplication.desktop().screenGeometry()
        x = screen_geo.width() - self.width() - 10
        y = 10
        self.move(x, y)

    # 鼠标按下事件
    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # 暂停动画
            if hasattr(self, "animation") and self.animation.state() == QPropertyAnimation.Running:
                self.animation.pause()

            # 保存鼠标相对窗口左上角的位置
            self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()
            event.accept()

    # 鼠标移动事件
    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton and self.dragPosition:
            self.move(event.globalPos() - self.dragPosition)
            event.accept()

    # 鼠标释放
    def mouseReleaseEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            # 更新动画的位置
            if hasattr(self, "animation"):
                self.update_animation_start_position()

            # 鼠标释放后恢复动画
            if hasattr(self, "animation") and self.animation.state() == QPropertyAnimation.Paused:
                self.animation.resume()
            self.dragPosition = None
            event.accept()

    def show_main_window(self):
        logger.info("---- 双击悬浮球，打开主界面 ----")
        self.main_window.show()
        self.main_window.is_floating_ball_visible = False
        self.hide()

    # 鼠标双击，打开主界面
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.show_main_window()



