import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow
from src.util.init_db import InitDB
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
import  os
from src.util.load_font import load_external_font

def main():
    app = QApplication(sys.argv)
    # 初始化SQLite
    db_tool = InitDB(CommonUtil.get_db_full_path())
    db_tool.create_table()
    db_tool.close_connection()

    # 获取当前脚本所在目录，构建样式表文件的路径
    stylesheet_path = CommonUtil.get_resource_path(FsConstants.BASE_QSS_PATH)
    if os.path.exists(stylesheet_path):
        with open(stylesheet_path, "r", encoding='utf-8') as file:
            stylesheet = file.read()
            # 为应用程序设置样式表
            app.setStyleSheet(stylesheet)
    # 加载外部字体
    font_path = CommonUtil.get_resource_path(FsConstants.FONT_FILE_PATH)
    font_family = load_external_font(font_path)
    if font_family:
        app.setFont(QFont(font_family))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()