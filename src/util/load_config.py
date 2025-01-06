import os

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
    if sqlite_path:
        logger.info(f"获取ini配置文件中数据库的路径：{sqlite_path}")
    else:
        logger.info(f"ini配置文件中未配置数据库的路径！")
        # 使用内置配置路径
        data_path = FsConstants.SAVE_FILE_PATH_WIN if CommonUtil.check_win_os() else CommonUtil.get_mac_user_path()
        # 构建数据库文件的相对路径,假设数据库文件名为database.db
        sqlite_path =  os.path.join(data_path, FsConstants.DATABASE_FILE)
        logger.info(f"内置的数据库的路径：{sqlite_path}")
    return sqlite_path

