# macOS 打包
# nuitka-project-if: {OS} == "Darwin":
# 打包成.app程序时，是文件夹类型，只能使用 standalone
#    nuitka-project: --standalone
# macOS 必须参数
#    nuitka-project: --macos-create-app-bundle
#    nuitka-project: --macos-app-icon={MAIN_DIRECTORY}/resources/images/app.icns
# Windows 打包成单文件exe
# nuitka-project-if: {OS} == "Windows":
#    nuitka-project: --onefile
#    nuitka-project: --windows-icon-from-ico={MAIN_DIRECTORY}/resources/images/app.ico
# 特有配置  禁用命令窗口
#    nuitka-project: --windows-console-mode=disable

# 打包单文件的系统
# nuitka-project-if: {OS} in ("Linux", "FreeBSD", "OpenBSD"):
#    nuitka-project: --onefile

# 引入插件PySide6
# nuitka-project: --plugin-enable=pyside6
# 添加数据目录
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/resources=resources
# 添加数据文件
# nuitka-project: --include-data-files={MAIN_DIRECTORY}/app.ini=app.ini

# 配置flask
# nuitka-project: --follow-imports
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/templates=templates
# nuitka-project: --include-data-dir={MAIN_DIRECTORY}/static=static


import sys
from multiprocessing import freeze_support
import multiprocessing

from PySide6.QtGui import QFont, QPalette
from PySide6.QtWidgets import QApplication
from loguru import logger

from flask_server import start_flask_in_thread
from src.main_window import MainWindow
from src.util.app_init_util import AppInitUtil
from src.util.config_util import ConfigUtil
from src.util.init_db import InitDB
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
import  os

def exception_hook(exctype, value, traceback):
    logger.info("全局异常捕获:", exctype, value, traceback)
    sys.__excepthook__(exctype, value, traceback)
sys.excepthook = exception_hook

def main():
    app = QApplication(sys.argv)

    # 初始化数据库
    AppInitUtil.init_db()
    # 初始化配置文件
    AppInitUtil.write_init_file()

    # 启动 Flask 服务
    if ConfigUtil.get_ini_flask_checked():
        start_flask_in_thread()

    # 加载样式表文件
    AppInitUtil.load_external_stylesheet(app)
    # 获取系统的默认调色板
    #palette = QPalette()
    #app.setPalette(palette)


    # 加载外部字体
    font_family = AppInitUtil.load_external_font()
    if font_family:
        app.setFont(QFont(font_family))


    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    # 检查进程上下文是否已经设置，如果没有设置，则进行设置
    if not multiprocessing.get_start_method():
        #设置多进程启动方式为 spawn
        multiprocessing.set_start_method('spawn')
    #避免子进程重新加载主脚本
    freeze_support()

    main()
