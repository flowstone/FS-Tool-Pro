from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu

from src.about_window import AboutWindow
from src.const.fs_constants import FsConstants
import os

from src.option_general import OptionGeneral
from src.util.common_util import CommonUtil
from loguru import logger

from src.log_window import LogWindow


class MenuBar:
    def __init__(self, parent):
        self.parent = parent
        self.menu_bar = QMenuBar(self.parent)
        # 初始化日志窗口
        self.log_window = LogWindow()
        # 初始化首选项窗口
        self.option_general = OptionGeneral()
        self.about_window = AboutWindow()
        self._create_help_menu()

    def _create_help_menu(self):
        """创建帮助菜单"""
        help_menu = QMenu(FsConstants.TOOLBAR_HELP_TITLE, self.parent)

        # 创建菜单项
        readme_action = QAction("说明", self.parent)
        readme_action.triggered.connect(open_readme)

        # 创建首选项菜单项
        option_general_action = QAction("首选项", self.parent)
        option_general_action.triggered.connect(self.show_option_general)

        # 创建日志窗口菜单项
        open_log_action = QAction("日志", self.parent)
        open_log_action.triggered.connect(self.show_log_window)

        # 创建日志窗口菜单项
        about_action = QAction("关于", self.parent)
        about_action.triggered.connect(self.show_about_window)

        # 将菜单项添加到“帮助”菜单中
        help_menu.addAction(option_general_action)
        help_menu.addAction(open_log_action)
        help_menu.addAction(readme_action)
        help_menu.addAction(about_action)


        # 添加帮助菜单到菜单栏
        self.menu_bar.addMenu(help_menu)

        # 设置菜单栏
        self.parent.setMenuBar(self.menu_bar)

    def show_log_window(self):
        """显示日志窗口"""
        self.log_window.show()


    def show_option_general(self):
        """显示首选项窗口"""
        self.option_general.show()


    def show_about_window(self):
        self.about_window.show()

def open_readme():
    try:
        file_path = CommonUtil.get_resource_path(FsConstants.HELP_PDF_FILE_PATH)
        # 使用系统默认的 PDF 阅读器打开文件
        if CommonUtil.check_win_os():
            os.startfile(file_path)  # Windows 平台
        else:
            os.system(f"open '{file_path}'")  # MacOS 平台

    except Exception as e:
        logger.error(f"无法打开 PDF 文件: {str(e)}")
