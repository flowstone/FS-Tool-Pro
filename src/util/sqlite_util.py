import sqlite3
from src.util.common_util import CommonUtil
from loguru import logger

# 数据库工具类
class SQLiteTool:
    def __init__(self, db_path):
        """
        初始化数据库连接和游标
        :param db_path: SQLite数据库文件的路径
        """
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def create(self, table_name, data_dict):
        """
        向指定表中插入一条记录
        :param table_name: 表名
        :param data_dict: 包含字段名和对应值的字典，例如 {'name': 'John', 'age': 25}
        """
        columns = ', '.join(data_dict.keys())
        placeholders = ', '.join(['?' for _ in data_dict])
        values = tuple(data_dict.values())
        logger.info(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})")
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def read(self, table_name, columns='*', condition=None):
        """
        从指定表中读取记录
        :param table_name: 表名
        :param columns: 要读取的列名，默认为'*'（读取所有列），例如 'name, age'
        :param condition: 查询条件，格式为SQL语句中的WHERE子句部分，例如 "age > 20"，默认为None（读取所有记录）
        :return: 查询到的记录列表
        """
        sql = f"SELECT {columns} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()
    def read_page(self, table_name, columns='*', condition=None, page_size=None, page_num=None):
        """
        从指定表中读取记录
        :param table_name: 表名
        :param columns: 要读取的列名，默认为'*'（读取所有列），例如 'name, age'
        :param condition: 查询条件，格式为SQL语句中的WHERE子句部分，例如 "age > 20"，默认为None（读取所有记录）
        :param page_size: 每页显示的记录数量，若不传则不进行分页查询，读取所有满足条件的记录
        :param page_num: 页码，若不传则不进行分页查询，读取所有满足条件的记录，页码从1开始计数
        :return: 查询到的记录列表
        """
        sql = f"SELECT {columns} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        if page_size and page_num:
            offset = (page_num - 1) * page_size
            sql += f" ORDER BY id DESC LIMIT {page_size} OFFSET {offset}"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def read_one(self, table_name, columns='*', condition=None):
        """
        从指定表中读取记录
        :param table_name: 表名
        :param columns: 要读取的列名，默认为'*'（读取所有列），例如 'name, age'
        :param condition: 查询条件，格式为SQL语句中的WHERE子句部分，例如 "age > 20"，默认为None（读取所有记录）
        :return: 查询到的记录列表
        """
        sql = f"SELECT {columns} FROM {table_name}"
        if condition:
            sql += f" WHERE {condition}"
        self.cursor.execute(sql)
        return self.cursor.fetchone()
    def update(self, table_name, data_dict, condition):
        """
        更新指定表中的记录
        :param table_name: 表名
        :param data_dict: 包含要更新的字段名和对应新值的字典，例如 {'name': 'Updated John', 'age': 30}
        :param condition: 更新条件，格式为SQL语句中的WHERE子句部分，例如 "id = 1"
        """
        set_clause = ', '.join([f"{key} =?" for key in data_dict])
        values = tuple(data_dict.values())

        sql = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.cursor.execute(sql, values)
        self.conn.commit()

    def delete(self, table_name, condition):
        """
        删除指定表中的记录
        :param table_name: 表名
        :param condition: 删除条件，格式为SQL语句中的WHERE子句部分，例如 "id = 1"
        """
        sql = f"DELETE FROM {table_name} WHERE {condition}"
        self.cursor.execute(sql)
        self.conn.commit()

    def close(self):
        """
        关闭数据库连接和游标
        """
        self.cursor.close()
        self.conn.close()

# 示例用法
if __name__ == "__main__":

    # 假设数据库文件名为test.db，可根据实际情况替换
    db_tool = SQLiteTool(CommonUtil.get_db_full_path())

    # 创建操作示例
    #data_to_create = {'name': 'Alice', 'age': 28}
    #db_tool.create('users', data_to_create)

    # 读取操作示例
    #result_read = db_tool.read('users')
    #print("读取到的记录:", result_read)

    # 更新操作示例
    #data_to_update = {'age': 29}
    #condition_update = "name = 'Alice'"
    #db_tool.update('users', data_to_update, condition_update)

    # 删除操作示例
    #condition_delete = "id = '1'"
    #db_tool.delete('users', condition_delete)

    db_tool.close()