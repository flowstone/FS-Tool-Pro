import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSystemTrayIcon, QMenu, QAction, QMainWindow

from src.app_instance_config import app_instance_config

from PyQt5.QtGui import QIcon

from src.util.message_util import MessageUtil
from src.widget.app_mini import FloatingBall
from loguru import logger
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
from src.widget.app_icon_widget import AppIconWidget
from src.util.menu_bar import MenuBar

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.closeEvent = None
        self.tray_icon = None
        self.menubar = None
        self.floating_ball = FloatingBall(self)
        self.is_floating_ball_visible = False
        self.icon_config = app_instance_config
        # 使用字典动态管理所有应用实例
        self.app_instances = {config["key"]: None for config in self.icon_config}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        logger.info(f"调用了主界面的初始化,悬浮球标志位 = {self.is_floating_ball_visible}")
        self.setWindowTitle(FsConstants.APP_WINDOW_TITLE)
        #self.setFixedSize(FsConstants.APP_WINDOW_WIDTH, FsConstants.APP_WINDOW_HEIGHT)

        # ---- 工具栏 START
        self.menubar = MenuBar(self)
        # ---- 工具栏 END

        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))



        layout.addLayout(self.create_icon_grid())
        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        # 初始化应用托盘图标
        self.init_tray_menu()

        # 处理窗口关闭事件，使其最小化到托盘
        self.closeEvent = self.handle_close_event

    def create_icon_grid(self):
        """动态创建图标的网格布局"""
        main_layout = QGridLayout()
        main_layout.setSpacing(0)  # 去除格子之间的间隙
        # 遍历图标配置，动态添加到布局
        for index, config in enumerate(self.icon_config):
            row, col = divmod(index, 4)  # 每行4个图标
            app_icon = self.create_app_icon(config["icon"], config["title"], config["key"])
            main_layout.addWidget(app_icon, row, col)
        return main_layout

    def create_app_icon(self, icon_path, title, key):
        """创建单个应用图标组件"""
        app_icon = AppIconWidget(CommonUtil.get_button_ico_path(icon_path), title)
        app_icon.iconClicked.connect(lambda _, name=key: self.open_feature_window(name))
        return app_icon

    # 初始化应用托盘图标
    def init_tray_menu(self):
        logger.info("---- 初始化任务栏图标 ----")

        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(
            QIcon(CommonUtil.get_resource_path(FsConstants.APP_BAR_ICON_PATH)))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
        self.tray_icon.activated.connect(self.tray_icon_activated)

        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = QAction("主界面", self)
        show_action.triggered.connect(self.tray_menu_show_main)
        quit_action = QAction("退出", self)
        quit_action.triggered.connect(sys.exit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)



    # 从托盘菜单点击显示窗口
    def tray_menu_show_main(self):
        logger.info("---- 托盘菜单点击显示窗口 ----")
        # 悬浮球退出
        self.floating_ball.close()
        self.is_floating_ball_visible = False
        self.show()



    # 处理窗口关闭事件
    def handle_close_event(self, event):
        logger.info(f"开始关闭主窗口，悬浮球标志位 = ,{self.is_floating_ball_visible}")
        event.ignore()
        self.hide()
        self.tray_icon.show()

        if not self.is_floating_ball_visible:
            self.create_floating_ball()
        logger.info(f"成功关闭主窗口，悬浮球标志位 = {self.is_floating_ball_visible}")

    def create_floating_ball(self):
        logger.info("---- 创建悬浮球 ----")
        self.floating_ball.show()
        self.is_floating_ball_visible = True


    # 双击托盘，打开窗口
    def tray_icon_activated(self, reason):
        logger.info("---- 双击任务栏托盘，打开窗口 ----")
        # 悬浮球退出
        self.floating_ball.close()
        self.is_floating_ball_visible = False
        if reason == QSystemTrayIcon.DoubleClick:
           self.show()


    def open_feature_window(self, key):
        """打开对应的功能窗口"""
        logger.info(f"---- 按钮<{key}>被点击了 ----")

        if key not in self.app_instances:
            logger.warning(f"未找到对应的应用: {key}")
            return
        # 如果实例不存在，则动态创建
        if self.app_instances[key] is None:
            app_class = next((item["class"] for item in self.icon_config if item["key"] == key), None)
            if app_class:
                try:
                    self.app_instances[key] = app_class()
                    self.app_instances[key].closed_signal.connect(lambda: self.on_sub_window_closed(key))
                except Exception as e:
                    logger.error(f"加载应用<{key}>时发生错误: {e}")
                    MessageUtil.show_error_message(f"无法加载功能模块：{key}\n错误信息：{e}")
                    return
        # 显示窗口
        if self.app_instances[key]:
            try:
                if self.app_instances[key].isMinimized():
                    self.app_instances[key].showNormal()
                else:
                    self.app_instances[key].show()
                    self.app_instances[key].activateWindow()

            except Exception as e:
                logger.error(f"显示应用<{key}>窗口时发生错误: {e}")
                MessageUtil.show_error_message(f"无法打开窗口：{key}\n错误信息：{e}")


    def on_sub_window_closed(self,key):
        # 子窗口关闭后的处理
        logger.info(f"子窗口{key}已关闭")
        self.app_instances[key] = None  # 释放子窗口的引用