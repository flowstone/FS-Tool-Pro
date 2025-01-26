from PySide6.QtCore import QObject, Signal

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.ini_util import IniUtil  # 引入 ConfigUtil 类
from loguru import logger

#### 单例装饰器，解决信号槽绑定失效
def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)  # 只在第一次调用时实例化
        return instances[cls]

    # 保持对原类常量的访问
    wrapper.__name__ = cls.__name__
    wrapper.__doc__ = cls.__doc__
    wrapper.__dict__.update(cls.__dict__)  # 保持类的属性、方法等
    return wrapper

@singleton
class ConfigManager(QObject):
    ############# Config 常量 #################
    APP_MINI_MASK_CHECKED_KEY = "mini_mask_checked"
    APP_MINI_BREATHING_LIGHT_CHECKED_KEY = "mini_breathing_light_checked"
    APP_MINI_CHECKED_KEY = "mini_checked"
    APP_MINI_SIZE_KEY = "mini_size"
    APP_MINI_IMAGE_KEY = "mini_image"

    APP_TRAY_MENU_CHECKED_KEY = "tray_menu_checked"
    APP_TRAY_MENU_IMAGE_KEY = "tray_menu_image"

    APP_SQLITE_PATH_KEY = "sqlite.path"
    APP_FLASK_CHECKED_KEY = "flask.checked"
    APP_ICON_FONT_BOLD_CHECKED_KEY = "icon_font_bold"
    ############# Config 常量 #################

    # 配置更新信号
    config_updated = Signal(str, object)

    def __init__(self):
        super().__init__()
        logger.info("Config Manager初始化")

    @staticmethod
    def load_config():
        ini_mini_size = IniUtil.get_ini_app_param(IniUtil.APP_MINI_SIZE_KEY)
        ini_mini_image = IniUtil.get_ini_app_param(IniUtil.APP_MINI_IMAGE_KEY)
        mini_size = ini_mini_size if IniUtil.get_ini_app_param(
            IniUtil.APP_MINI_CHECKED_KEY) else FsConstants.APP_MINI_SIZE
        mini_image = ini_mini_image if IniUtil.get_ini_app_param(
            IniUtil.APP_MINI_CHECKED_KEY) else CommonUtil.get_resource_path(FsConstants.APP_MINI_ICON_FULL_PATH)

        ini_tray_menu_image = IniUtil.get_ini_app_param(IniUtil.APP_TRAY_MENU_IMAGE_KEY)
        tray_menu_image = ini_tray_menu_image if IniUtil.get_ini_app_param(
            IniUtil.APP_TRAY_MENU_CHECKED_KEY) else CommonUtil.get_resource_path(FsConstants.APP_BAR_ICON_FULL_PATH)

        ini_sqlite_path = IniUtil.get_ini_app_param(IniUtil.APP_SQLITE_PATH_KEY)
        sql_path = ini_sqlite_path if ini_sqlite_path else CommonUtil.get_sqlite_dir()
        # 从 INI 文件加载配置
        config = {
            ConfigManager.APP_MINI_MASK_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_MINI_MASK_CHECKED_KEY),
            ConfigManager.APP_MINI_BREATHING_LIGHT_CHECKED_KEY: IniUtil.get_ini_app_param(
                IniUtil.APP_MINI_BREATHING_LIGHT_CHECKED_KEY),

            ConfigManager.APP_MINI_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_MINI_CHECKED_KEY),
            ConfigManager.APP_MINI_SIZE_KEY: mini_size,
            ConfigManager.APP_MINI_IMAGE_KEY: mini_image,
            ConfigManager.APP_TRAY_MENU_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_TRAY_MENU_CHECKED_KEY),
            ConfigManager.APP_TRAY_MENU_IMAGE_KEY: tray_menu_image,

            ConfigManager.APP_SQLITE_PATH_KEY: sql_path,
            ConfigManager.APP_FLASK_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_FLASK_CHECKED_KEY),
            ConfigManager.APP_ICON_FONT_BOLD_CHECKED_KEY: IniUtil.get_ini_app_param(IniUtil.APP_ICON_FONT_BOLD_CHECKED_KEY),

        }
        return config

    def save_config(self, key, value):
        if key == ConfigManager.APP_MINI_MASK_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_MINI_MASK_CHECKED_KEY, value)
        elif key == ConfigManager.APP_MINI_BREATHING_LIGHT_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_MINI_BREATHING_LIGHT_CHECKED_KEY, value)
        elif key == ConfigManager.APP_MINI_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_MINI_CHECKED_KEY, value)
        elif key == ConfigManager.APP_MINI_SIZE_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_MINI_SIZE_KEY, value)
        elif key == ConfigManager.APP_MINI_IMAGE_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_MINI_IMAGE_KEY, value)
        elif key == ConfigManager.APP_TRAY_MENU_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_TRAY_MENU_CHECKED_KEY, value)
        elif key == ConfigManager.APP_TRAY_MENU_IMAGE_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_TRAY_MENU_IMAGE_KEY, value)

        # elif key == ConfigManager.APP_SQLITE_PATH_KEY:
        #     IniUtil.set_ini_app_param(IniUtil.APP_SQLITE_PATH_KEY, value)
        elif key == ConfigManager.APP_FLASK_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_FLASK_CHECKED_KEY, value)
        elif key == ConfigManager.APP_ICON_FONT_BOLD_CHECKED_KEY:
            IniUtil.set_ini_app_param(IniUtil.APP_ICON_FONT_BOLD_CHECKED_KEY, value)


        self.config_updated.emit(key, value)  # 发出配置更新信号

    def get_config(self, key):
        config = self.load_config()
        return config.get(key)

    def set_config(self, key, value):
        self.save_config(key, value)
