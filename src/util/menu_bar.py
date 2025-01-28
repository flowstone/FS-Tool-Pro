from PySide6.QtGui import QAction
from PySide6.QtWidgets import QMenuBar, QMenu
from fs_base.base_menu_bar import BaseMenuBar

from src.about_window import AboutWindow
from src.const.fs_constants import FsConstants
import os

from src.option_general import OptionGeneral
from src.util.common_util import CommonUtil
from loguru import logger

from src.log_window import LogWindow


class MenuBar(BaseMenuBar):
    def __init__(self, parent):
        super().__init__(parent)
        self.log_window = LogWindow()
        self.option_tab = OptionGeneral()
        self.about_window = AboutWindow()

    def show_log_window(self):
        """显示日志窗口"""
        self.log_window.show()

    def show_option_tab(self):
        """显示首选项窗口"""
        self.option_tab.show()

    def show_about_window(self):
        self.about_window.show()

