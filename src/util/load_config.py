import configparser
import os
from io import StringIO

from loguru import logger


# 从 INI 文件加载用设置
def get_ini_config():
    """
    获取 INI 文件的配置对象，如果文件不存在则初始化。
    """
    from src.util.common_util import CommonUtil
    ini_path = CommonUtil.get_app_ini_path()
    config = configparser.ConfigParser(allow_no_value=True)

    if not os.path.exists(ini_path):
        # 如果文件不存在，创建一个空配置文件
        with open(ini_path, "w", encoding="utf-8") as f:
            f.write("; 应用配置文件\n")
    else:
        config.read(ini_path, encoding="utf-8")
    return config, ini_path

# 从 INI 文件加载用设置
def get_ini_sqlite_path():
    """
    从 INI 文件加载 SQLite 的路径
    """
    config, _ = get_ini_config()
    return config.get("SQLite", "path", fallback="")

# 从 INI 文件读取各个应用是否显示的配置
def get_ini_app_visibility():
    """
    从 INI 文件读取各个应用是否显示的配置
    """
    from src.app_instance_config import app_instance_config
    config, _ = get_ini_config()
    visibility_config = {}

    if "Apps" not in config.sections():
        config.add_section("Apps")
    for app in app_instance_config:
        key = app['key']
        is_visible = config.getboolean("Apps", f"{key}.is_visible", fallback=True)
        visibility_config[key] = is_visible

    return visibility_config

#  从 INI 文件读取 Flask 服务是否启用的配置
def get_ini_flask_flag():
    """
    从 INI 文件读取 Flask 服务是否启用的配置
    """
    config, _ = get_ini_config()
    return config.getboolean("Flask", "flag", fallback=True)

# 将应用可见性写入到 INI 配置文件中
def set_ini_flask_flag(enabled):
    """
    将 Flask 服务的启用状态写入到 INI 配置文件中，保留注释。
    :param enabled: bool, True 表示启用 Flask 服务，False 表示禁用。
    """
    config, ini_path = get_ini_config()
    # 更新配置值
    update_ini_line(ini_path, "Flask", "flag", "true" if enabled else "false")
    logger.info(f"Flask 服务状态已更新为: {'启用' if enabled else '禁用'}")

def update_ini_line(ini_path, section, key, value):
    """
    在 INI 文件中修改指定配置项的值，仅修改目标行，保留其他内容（包括注释和空行）。

    :param ini_path: str, INI 文件路径。
    :param section: str, 目标配置节名称（如 "Flask"）。
    :param key: str, 配置项的键名（如 "flag"）。
    :param value: str, 配置项的新值。
    """
    if not os.path.exists(ini_path):
        raise FileNotFoundError(f"配置文件 {ini_path} 不存在！")

    with open(ini_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    updated = False
    in_target_section = False
    section_header = f"[{section}]"
    new_line = f"{key} = {value}\n"

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        # 检测到目标节
        if stripped_line == section_header:
            in_target_section = True
            continue

        # 检测到目标键，并处于目标节
        if in_target_section and stripped_line.startswith(f"{key}"):
            lines[i] = new_line
            updated = True
            break

        # 检测到新节开始，退出目标节
        if in_target_section and stripped_line.startswith("[") and stripped_line != section_header:
            break

    # 如果没有找到目标节或键，则新增
    if not updated:
        if not in_target_section:
            lines.append(f"\n{section_header}\n")
        lines.append(new_line)

    # 写回修改后的文件
    with open(ini_path, "w", encoding="utf-8") as f:
        f.writelines(lines)
