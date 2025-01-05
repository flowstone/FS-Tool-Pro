from PySide6.QtCore import QSettings
from loguru import logger

from src.const.fs_constants import FsConstants


def get_sqlite_path():
    """
    从 INI 文件加载用户设置（程序启动时自动调用）
    """
    from src.util.common_util import CommonUtil

    # 创建 QSettings 对象
    settings = QSettings(CommonUtil.get_resource_path(FsConstants.APP_INI_FILE), QSettings.Format.IniFormat)

    # 读取设置
    sqlite_path = settings.value("SQLite/path", "")
    logger.info(f"获取ini文件中数据库的路径：{sqlite_path}")
    return sqlite_path

