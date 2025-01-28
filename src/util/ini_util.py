

from fs_base.app_ini_util import AppIniUtil



class IniUtil(AppIniUtil):




    # 从 INI 文件读取各个应用是否显示的配置
    @staticmethod
    def get_ini_app_visibility():
        """
        从 INI 文件读取各个应用是否显示的配置
        """
        from src.app_instance_config import app_instance_config
        config, _ = IniUtil.get_ini_config()
        visibility_config = {}

        if "Apps" not in config.sections():
            config.add_section("Apps")
        for app in app_instance_config:
            key = app['key']
            is_visible = config.getboolean("Apps", f"{key}.is_visible", fallback=True)
            visibility_config[key] = is_visible

        return visibility_config
