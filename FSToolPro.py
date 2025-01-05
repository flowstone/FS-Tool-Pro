# Nuitka options. These determine compilation settings based on the current OS.
# nuitka-project-if: {OS} == "Darwin":
#    nuitka-project: --standalone
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/resources/images/app.icns
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --onefile
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/resources/images/app.ico
#    nuitka-project: --windows-console-mode=disable
# nuitka-project-if: {OS} in ("Linux", "FreeBSD", "OpenBSD"):
#    nuitka-project: --onefile

# These are standard options that are needed on all platforms.
# nuitka-project: --plugin-enable=pyside6

# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/resources=resources
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/app.ini=app.ini



import sys

from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import QApplication
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
    # 获取系统的默认调色板
    palette = QPalette()
    app.setPalette(palette)

    # 加载外部字体
    font_path = CommonUtil.get_resource_path(FsConstants.FONT_FILE_PATH)
    font_family = load_external_font(font_path)
    if font_family:
        app.setFont(QFont(font_family))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()