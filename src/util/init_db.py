from loguru import logger

from src.util.common_util import CommonUtil
from src.util.config_util import ConfigUtil
from src.util.sqlite_connection_pool import SQLiteConnectionPool


class InitDB:
    def __init__(self, db_name):
        """
        初始化数据库连接和游标
        """
        self.db_pool = SQLiteConnectionPool(db_name, pool_size=3)

    def create_table(self):
        """
        创建users表，如果不存在的话
        """
        connection = self.db_pool.get_connection()
        try:
            cursor = connection.cursor()
            create_table_sql = '''
            CREATE TABLE IF NOT EXISTS auto_answers_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                error INTEGER DEFAULT 0, 
                success INTEGER DEFAULT 0,
                today CHAR COMMENT '今天时间' NOT NULL UNIQUE,
                create_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            '''
            cursor.execute(create_table_sql)
            connection.commit()
        except Exception as e:
            logger.warning(f"创建表失败：{str(e)}")
        finally:
            self.db_pool.release_connection(connection)

    def drop_table(self):
        connection = self.db_pool.get_connection()
        try:
            cursor = connection.cursor()
            drop_table_sql = "DROP TABLE IF EXISTS users"
            cursor.execute(drop_table_sql)
            connection.commit()
        except Exception as e:
            logger.warning(f"删除表失败：{str(e)}")
        finally:
            self.db_pool.release_connection(connection)

    def close_connection(self):
        """
        关闭数据库连接
        """
        self.db_pool.close_all()


# 示例用法
if __name__ == "__main__":
    db_tool = InitDB(ConfigUtil.get_db_full_path())
    db_tool.create_table()
    #db_tool.drop_table()
    # 关闭连接
    db_tool.close_connection()