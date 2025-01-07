import os

from PySide6.QtCore import QSettings
from loguru import logger

from src.const.fs_constants import FsConstants

# 从 INI 文件加载用设置
def get_sqlite_path():
    """
    从 INI 文件加载用户设置（程序启动时自动调用）
    """
    from src.util.common_util import CommonUtil
    # 创建 QSettings 对象
    settings = QSettings(CommonUtil.get_app_ini_path(), QSettings.Format.IniFormat)
    # 读取设置
    sqlite_path = settings.value("SQLite/path", "")
    return sqlite_path



