import json
from loguru import logger


class ConfigManager:

    def __init__(self, config_file_path='config.json'):

        try:
            with open(config_file_path, 'r') as file:
                config = json.load(file)
                self.__db_location = config['database']['location']
                self.__answer_pwd = config['AutoAnswers']['password']
                self.__answer_driver = config['AutoAnswers']['driver']
        except FileNotFoundError:
            logger.error(f"配置文件 {config_file_path} 不存在，请检查文件路径是否正确。")
        except KeyError as e:
            logger.error(f"配置文件 {config_file_path} 中缺少必要的键 {e}，请检查配置文件内容。")
        except json.JSONDecodeError:
            logger.error(f"配置文件 {config_file_path} 格式有误，无法正确解析 JSON 数据，请检查文件格式。")

    def get_db_location(self):
        return self.__db_location

    def get_answer_pwd(self):
        return self.__answer_pwd

    def get_answer_driver(self):
        return self.__answer_driver
