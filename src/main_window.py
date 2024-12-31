import sys
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QSystemTrayIcon, QMenu, QAction, QMainWindow

from src.batch_heic_jpg import HeicToJpgApp
from src.desktop_clock import ColorSettingDialog
from src.pic_conversion import PicConversionApp
from src.batch_file_renamer import RenameFileApp
from src.batch_create_folder import CreateFolderApp
from src.stick_note import StickyNoteApp
from src.password_generator import  PasswordGeneratorApp
from src.file_comparator import FileComparatorApp
from src.file_generator import FileGeneratorApp
from src.file_encryptor import FileEncryptorApp
from src.rsa_key_generator import RSAKeyGeneratorApp
from src.hash_calculator import HashCalculatorApp

from PyQt5.QtGui import QIcon
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
        self.icon_config = None
        # 使用字典动态管理所有应用实例
        self.app_instances = {
            "desktop_clock": None,
            "pic_conversion": None,
            "create_folder": None,
            "rename_file": None,
            "heic_to_jpg": None,
            "stick_note": None,
            "password_generator": None,
            "file_generator": None,
            "file_comparator": None,
            "file_encryptor": None,
            "rsa_key_generator": None,
            "hash_calculator": None
        }
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

        # 图标配置：每个图标包含路径、标题、点击事件
        self.icon_config = [
            {"key": "desktop_clock", "icon": FsConstants.BUTTON_TIME_ICON, "title": FsConstants.DESKTOP_CLOCK_WINDOW_TITLE,
            "class": ColorSettingDialog},
            {"key": "stick_note", "icon": FsConstants.BUTTON_STICK_NOTE_ICON, "title": FsConstants.STICK_NOTE_WINDOW_TITLE,
             "class": StickyNoteApp},
            {"key": "password_generator", "icon": FsConstants.BUTTON_PASSWORD_ICON, "title": FsConstants.PASSWORD_GENERATOR_TITLE,
             "class": PasswordGeneratorApp},
            {"key": "create_folder", "icon": FsConstants.BUTTON_FOLDER_ICON, "title": FsConstants.CREATE_FOLDER_WINDOW_TITLE,
            "class": CreateFolderApp},
            {"key": "rename_file","icon": FsConstants.BUTTON_FILE_ICON, "title": FsConstants.FILE_RENAMER_WINDOW_TITLE,
            "class": RenameFileApp},
            {"key": "heic_to_jpg", "icon": FsConstants.BUTTON_HEIC_ICON, "title": FsConstants.HEIC_JPG_BUTTON_TITLE,
            "class": HeicToJpgApp},
            {"key": "pic_conversion","icon": FsConstants.BUTTON_PIC_ICON, "title": FsConstants.PIC_CONVERSION_WINDOW_TITLE,
            "class": PicConversionApp},
            {"key": "file_generator", "icon": FsConstants.BUTTON_FILE_GENERATOR_ICON, "title": FsConstants.FILE_GENERATOR_WINDOW_TITLE,
            "class": FileGeneratorApp},
            {"key": "file_comparator", "icon": FsConstants.BUTTON_FILE_COMPARATOR_ICON, "title": FsConstants.FILE_COMPARATOR_WINDOW_TITLE,
            "class": FileComparatorApp},
            {"key": "file_encryptor", "icon": FsConstants.BUTTON_FILE_ENCRYPTOR_ICON, "title": FsConstants.FILE_ENCRYPTOR_WINDOW_TITLE,
             "class": FileEncryptorApp},
            {"key": "rsa_key_generator", "icon": FsConstants.BUTTON_RSA_KEY_GENERATOR_ICON,"title": FsConstants.RSA_KEY_GENERATOR_WINDOW_TITLE,
             "class": RSAKeyGeneratorApp},
            {"key": "hash_calculator", "icon": FsConstants.BUTTON_HASH_CALCULATOR_ICON,"title": FsConstants.HASH_CALCULATOR_WINDOW_TITLE,
             "class": HashCalculatorApp},
        ]


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
            QIcon(CommonUtil.get_mini_ico_full_path()))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
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
        logger.info(f"成功关闭主窗口，悬浮球标志位 = ,{self.is_floating_ball_visible}")

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
                self.app_instances[key] = app_class()
                self.app_instances[key].closed_signal.connect(lambda: self.on_sub_window_closed(key))
        # 显示窗口
        if self.app_instances[key]:
            if self.app_instances[key].isMinimized():
                self.app_instances[key].showNormal()
            else:
                self.app_instances[key].show()
                self.app_instances[key].activateWindow()

    def on_sub_window_closed(self,key):
        # 子窗口关闭后的处理
        logger.info(f"子窗口{key}已关闭")
        self.app_instances[key] = None  # 释放子窗口的引用