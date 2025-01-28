import sys
import os
import datetime
import socket

from fs_base.base_util import BaseUtil
from loguru import logger
from src.const.fs_constants import FsConstants


class CommonUtil(BaseUtil):

    # 获得按钮小图标全路径
    @staticmethod
    def get_button_ico_path(app_icon):
        full_path = os.path.join(FsConstants.APP_ICON_RESOURCE_PATH, app_icon)
        return CommonUtil.get_resource_path(full_path)

    # 获得Fast Sender全路径
    @staticmethod
    def get_fast_sender_dir():
        # 使用内置配置路径
        data_path = CommonUtil.get_external_path()
        return os.path.join(data_path, FsConstants.EXTERNAL_FAST_SENDER_DIR)

    # 获得Flask Mini全路径
    @staticmethod
    def get_flask_mini_dir():
        # 使用内置配置路径
        data_path = CommonUtil.get_external_path()
        return os.path.join(data_path, FsConstants.EXTERNAL_FLASK_MINI_DIR)


    # 获得Fast Sender全路径
    @staticmethod
    def get_sqlite_dir():
        # 使用内置配置路径
        data_path = CommonUtil.get_external_path()
        return os.path.join(data_path, FsConstants.EXTERNAL_DATABASE_FILE)