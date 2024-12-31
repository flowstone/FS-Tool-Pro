import sys
import os
import datetime


from src.const.fs_constants import FsConstants
from src.util.config_manager import ConfigManager

class CommonUtil:

    # 获取资源（如图片等）的实际路径，处理打包后资源路径的问题
    @staticmethod
    def get_resource_path(relative_path):
        """
        获取资源（如图片等）的实际路径，处理打包后资源路径的问题
        """
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)

        if CommonUtil.check_win_os():
            #return os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)
            return os.path.join(os.path.dirname(sys.argv[0]), relative_path)
        else:
            return os.path.join(os.path.dirname(sys.argv[0]), relative_path)

    # 当前系统是Win 返回True
    @staticmethod
    def check_win_os():
        return sys.platform.startswith('win')


    #获得应用图标全路径
    @staticmethod
    def get_ico_full_path():
        return CommonUtil.get_resource_path(FsConstants.APP_ICON_PATH)

    # 获得应用小图标全路径
    @staticmethod
    def get_mini_ico_full_path():
        return CommonUtil.get_resource_path(FsConstants.APP_MINI_ICON_PATH)

    # 获得Loading
    @staticmethod
    def get_loading_full_path():
        return CommonUtil.get_resource_path(FsConstants.LOADING_PATH)
    # 获得数据库文件全路径
    @staticmethod
    def get_db_full_path():
        # 读取配置文件
        config_manager = ConfigManager(CommonUtil.get_resource_path(FsConstants.APP_CONFIG_FILE))
        db_location = config_manager.get_db_location()
        if db_location:
            return db_location

        # 使用内置配置路径
        data_path = FsConstants.SAVE_FILE_PATH_WIN if CommonUtil.check_win_os() else CommonUtil.get_mac_user_path()
        # 构建数据库文件的相对路径,假设数据库文件名为database.db
        return os.path.join(data_path, FsConstants.DATABASE_FILE)

    # 静止外部类调用这个方法
    @staticmethod
    def get_mac_user_path():
        return os.path.expanduser(FsConstants.SAVE_FILE_PATH_MAC)

    # 获得当前日期
    @staticmethod
    def get_today():
        # 获取当前日期（是一个date对象）
        current_date = datetime.date.today()
        # 使用strftime方法按照指定格式进行格式化
        return current_date.strftime('%Y-%m-%d')

    # 获得当前指定格式的时间
    # %Y-%m-%d %H:%M:%S
    @staticmethod
    def get_current_time(format:str='%Y-%m-%d %H:%M:%S'):
        # 获取当前日期和时间
        current_datetime = datetime.datetime.now()

        # 格式化时间为指定格式
        return current_datetime.strftime(format)

    #递归函数来遍历文件夹及其子文件夹中的所有文件
    @staticmethod
    def count_files_recursive(folder_path:str):
        """
        递归函数来遍历文件夹及其子文件夹中的所有文件
        """
        count = 0
        for root, dirs, files in os.walk(folder_path):
            count += len(files)
        return count

    # 遍历文件夹的所有文件
    @staticmethod
    def count_files_in_folder(folder_path: str):
        """
        统计指定文件夹下文件的个数（不进入子文件夹统计）
        """
        file_count = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                file_count += 1
        return file_count

    # 统计文件夹下的所有文件夹总数
    @staticmethod
    def count_folders_in_folder(folder_path: str):
        """
        统计指定文件夹下的文件夹数量（不进入子文件夹统计）
        """
        folder_count = 0
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                folder_count += 1
        return folder_count

    # 获得Chrome Driver全路径
    @staticmethod
    def get_chrome_driver_path():
        # 读取配置文件
        config_manager = ConfigManager(CommonUtil.get_resource_path(FsConstants.APP_CONFIG_FILE))
        answer_driver = config_manager.get_answer_driver()
        if answer_driver:
            return answer_driver

        # 使用内置配置路径
        data_path = FsConstants.AUTO_ANSWERS_WIN_DRIVER_NAME if CommonUtil.check_win_os() else FsConstants.AUTO_ANSWERS_OTHER_DRIVER_NAME
        full_path =os.path.join(FsConstants.AUTO_ANSWERS_DRIVER_PATH, data_path)
        return CommonUtil.get_resource_path(full_path)

    # 获得按钮小图标全路径
    @staticmethod
    def get_button_ico_path(button_icon):
        full_path = os.path.join(FsConstants.BUTTON_ICON_PATH, button_icon)
        return CommonUtil.get_resource_path(full_path)

    @staticmethod
    def format_time(current_datetime):
        format: str = '%Y-%m-%d %H:%M:%S'
        # 将时间戳转换为datetime对象
        dt_object = datetime.datetime.fromtimestamp(current_datetime)
        # 格式化时间，这里使用了常见的年-月-日 时:分:秒格式
        # 格式化时间为指定格式
        return dt_object.strftime(format)