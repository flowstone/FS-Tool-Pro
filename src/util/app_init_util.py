import os
import shutil
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from PySide6.QtGui import QFontDatabase, QPalette
from loguru import logger

from src.util.config_manager import ConfigManager
from src.util.init_db import InitDB


# 初始化文件
class AppInitUtil:

    # 初始化文件
    @staticmethod
    def write_init_file():

        external_fast_sender_dir = CommonUtil.get_fast_sender_dir()
        external_flask_mini_dir = CommonUtil.get_flask_mini_dir()
        # 创建Fast Sender文件夹
        if not os.path.exists(external_fast_sender_dir):
            logger.info(f"创建Fast Sender文件夹:{external_fast_sender_dir}")
            os.makedirs(external_fast_sender_dir)
        # 创建Flask Mini文件夹
        if not os.path.exists(external_flask_mini_dir):
            logger.info(f"创建Flask Mini文件夹:{external_flask_mini_dir}")
            os.makedirs(external_flask_mini_dir)

        # 复制app.ini文件
        source_file = CommonUtil.get_resource_path(FsConstants.APP_INI_FILE)
        destination_file = os.path.join(CommonUtil.get_external_path(), FsConstants.EXTERNAL_APP_INI_FILE)
        # 如果目标文件不存在，则复制
        if not os.path.exists(destination_file):
            logger.info(f"复制app.ini文件:{source_file} -> {destination_file}")
            shutil.copyfile(source_file, destination_file)

    @staticmethod
    def load_external_stylesheet(app):
        # 加载样式表文件
        stylesheet_path = CommonUtil.get_resource_path(FsConstants.BASE_QSS_PATH)
        if os.path.exists(stylesheet_path):
            with open(stylesheet_path, "r", encoding='utf-8') as file:
                stylesheet = file.read()
                # 为应用程序设置样式表
                app.setStyleSheet(stylesheet)

    # 加载外部字体
    @staticmethod
    def load_external_font():
        font_path = CommonUtil.get_resource_path(FsConstants.FONT_FILE_PATH)
        font_id = QFontDatabase.addApplicationFont(font_path)
        if font_id == -1:
            logger.warning("字体加载失败")
        else:
            logger.info("字体加载成功")
            font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
            return font_family

    # 初始化数据库
    @staticmethod
    def init_db():
        config_manager = ConfigManager()
        load_db = InitDB(config_manager.get_config(ConfigManager.APP_SQLITE_PATH_KEY))
        load_db.create_table()
        load_db.close_connection()