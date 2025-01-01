import sys

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication
from src.main_window import MainWindow
from src.util.load_db import LoadDB
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
import  os
from src.util.load_font import load_external_font

def main():
    app = QApplication(sys.argv)

    # 初始化数据库
    load_db = LoadDB(CommonUtil.get_db_full_path())
    load_db.create_table()
    load_db.close_connection()

    # 加载样式表文件
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