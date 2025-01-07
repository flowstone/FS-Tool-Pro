import os
import shutil
from loguru import logger
from src.const.fs_constants import FsConstants

# 初始化文件
def write_init_file():
    from src.util.common_util import CommonUtil

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


