from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QMouseEvent, QPixmap
from loguru import logger
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil

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

        self.setWindowOpacity(0.8)  # 设置透明度

        self.setup_background_image()
        self.move_to_top_right()

        self.dragPosition = None
        self.setMouseTracking(True)



        # 启动呼吸灯效果（透明度周期性变化）
        self.breathing_light_window()

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
            self.dragPosition = None

    def show_main_window(self):
        logger.info("---- 双击悬浮球，打开主界面 ----")
        self.main_window.show()
        self.main_window.is_floating_ball_visible = False
        #self.close()
        self.hide()

    # 鼠标双击，打开主界面
    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.show_main_window()



