import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTabWidget
from fs_base.widget import TabAnimation
from loguru import logger

from src.const.fs_constants import FsConstants
from src.image_convert import ImageConvertApp
from src.image_heic_jpg import HeicToJpgApp
from src.invisible_watermark import InvisibleWatermarkApp
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class ImageToolApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IMAGE_TOOL} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_IMAGE_TOOL)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)
        self.setMinimumWidth(600)
        # 创建主布局
        layout = QVBoxLayout(self)
        # 创建 TabWidget
        self.tab_widget = TabAnimation()
        # 添加标签页
        self.add_tabs()
        # 将 TabWidget 添加到布局
        layout.addWidget(self.tab_widget)
        # 设置主窗口布局
        self.setLayout(layout)


    def add_tabs(self):
        self.tab_widget.addTab(ImageConvertApp(), "图片转换")
        self.tab_widget.addTab(HeicToJpgApp(), "HEIC转JPG")
        self.tab_widget.addTab(InvisibleWatermarkApp(), "隐水印")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageToolApp()
    window.show()
    sys.exit(app.exec())