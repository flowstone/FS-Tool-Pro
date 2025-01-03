import sys

from PyQt5.QtCore import pyqtSignal, QObject
from PyQt5.QtWidgets import QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon
from loguru import logger
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants


class TrayMenu(QObject):
    show_main_signal = pyqtSignal()
    activated_signal = pyqtSignal()
    quit_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.tray_icon = None

    def init_tray_menu(self, main_window):
        logger.info("---- 初始化任务栏图标 ----")
        # 创建系统托盘图标
        self.tray_icon = QSystemTrayIcon(main_window)
        self.tray_icon.setIcon(
            QIcon(CommonUtil.get_resource_path(FsConstants.APP_BAR_ICON_FULL_PATH)))  # 这里需要一个名为icon.png的图标文件，可以替换为真实路径
        # 双击托盘图标，打开主界面
        self.tray_icon.activated.connect(lambda: self.activated_signal.emit())

        # 创建托盘菜单
        tray_menu = QMenu()
        show_action = QAction("主界面", main_window)
        show_action.triggered.connect(lambda: self.show_main_signal.emit())
        quit_action = QAction("退出", main_window)
        quit_action.triggered.connect(sys.exit)
        tray_menu.addAction(show_action)
        tray_menu.addAction(quit_action)
        self.tray_icon.setContextMenu(tray_menu)
        self.tray_icon.show()

