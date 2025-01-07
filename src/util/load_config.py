import os

from PySide6.QtCore import QSettings
from loguru import logger

from src.const.fs_constants import FsConstants

# 从 INI 文件加载用设置
def get_ini_sqlite_path():
    """
    从 INI 文件加载用户设置（程序启动时自动调用）
    """
    from src.util.common_util import CommonUtil
    # 创建 QSettings 对象
    settings = QSettings(CommonUtil.get_app_ini_path(), QSettings.Format.IniFormat)
    # 读取设置
    sqlite_path = settings.value("SQLite/path", "")
    return sqlite_path

# 从 INI 文件读取各个应用是否显示的配置
def get_ini_app_visibility():
    """
    从 INI 文件读取各个应用是否显示的配置
    """
    from src.app_instance_config import app_instance_config
    from src.util.common_util import CommonUtil
    settings = QSettings(CommonUtil.get_app_ini_path(), QSettings.Format.IniFormat)

    visibility_config = {}
    for config in app_instance_config:
        # 从配置文件读取是否显示，默认值为 True
        is_visible = settings.value(f"Apps/{config['key']}.is_visible", True)
        # 将字符串 "true" 或 "false" 转换为布尔值
        is_visible = str(is_visible).strip().lower() == "true"
        visibility_config[config['key']] = is_visible

    return visibility_config
