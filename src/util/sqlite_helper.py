from PyQt5.QtCore import QObject, pyqtSignal
from loguru import logger
from src.util.sqlite_connection_pool import SQLiteConnectionPool


class SQLiteHelper(QObject):
    # 数据查询信号
    data_fetched = pyqtSignal(list)
    single_row_fetched = pyqtSignal(tuple)
    paginated_data_fetched = pyqtSignal(list, int)  # 信号：数据列表和总页数

    def __init__(self, db_name):
        super().__init__()
        self.db_pool = SQLiteConnectionPool(db_name, pool_size=3)

    # 创建表
    def create_table(self, table_name, columns):
        """
        创建表格
        :param table_name: 表名
        :param columns: 字段描述字典 {字段名: 字段类型}
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()
            columns_definition = ", ".join([f"{col} {typ}" for col, typ in columns.items()])
            sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_definition});"

            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.warning(f"创建表失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)

    # 插入数据
    def insert_data(self, table_name, data):
        """
        插入数据
        :param table_name: 表名
        :param data: 数据字典 {字段名: 值}
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            columns = ", ".join(data.keys())
            placeholders = ", ".join(["?" for _ in data])
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

            cursor.execute(sql, tuple(data.values()))
            conn.commit()
        except Exception as e:
            logger.warning(f"插入数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)


    # 查询数据（多条记录）
    def fetch_data(self, table_name, columns="*", condition=""):
        """
        查询数据（多条记录）
        :param table_name: 表名
        :param columns: 选择的列（默认为 *）
        :param condition: 查询条件（可选）
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            sql = f"SELECT {columns} FROM {table_name} {condition};"
            cursor.execute(sql)

            result = cursor.fetchall()
            self.data_fetched.emit(result)  # 通过信号发送数据

        except Exception as e:
            logger.warning(f"查询数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)


    # 查询单条记录
    def fetch_one(self, table_name, columns="*", condition=""):
        """
        查询单条数据
        :param table_name: 表名
        :param columns: 选择的列（默认为 *）
        :param condition: 查询条件（可选）
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            sql = f"SELECT {columns} FROM {table_name} {condition} LIMIT 1;"
            cursor.execute(sql)

            result = cursor.fetchone()
            self.single_row_fetched.emit(result)  # 通过信号发送单条数据

        except Exception as e:
            logger.warning(f"查询单条数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)

    # 分页查询
    def fetch_paginated_data(self, table_name, columns="*", page=1, page_size=10, condition=""):
        """
        分页查询数据
        :param table_name: 表名
        :param columns: 选择的列（默认为 *）
        :param page: 当前页码（从 1 开始）
        :param page_size: 每页记录数
        :param condition: 查询条件（可选）
        """
        offset = (page - 1) * page_size
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            # 查询当前页数据
            sql = f"SELECT {columns} FROM {table_name} {condition} LIMIT {page_size} OFFSET {offset};"
            cursor.execute(sql)
            result = cursor.fetchall()

            # 查询总记录数
            count_sql = f"SELECT COUNT(*) FROM {table_name} {condition};"
            cursor.execute(count_sql)
            total_records = cursor.fetchone()[0]
            total_pages = (total_records + page_size - 1) // page_size  # 计算总页数

            # 发出分页数据和总页数
            self.paginated_data_fetched.emit(result, total_pages)
        except Exception as e:
            logger.warning(f"分页查询数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)



    # 更新数据
    def update_data(self, table_name, data, condition):
        """
        更新数据
        :param table_name: 表名
        :param data: 更新的数据字典 {字段名: 值}
        :param condition: 更新条件，例如 "WHERE id = ?"
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()

            set_clause = ", ".join([f"{key} = ?" for key in data.keys()])
            sql = f"UPDATE {table_name} SET {set_clause} {condition}"

            cursor.execute(sql, tuple(data.values()))
            conn.commit()
        except Exception as e:
            logger.warning(f"更新数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)


    # 删除数据
    def delete_data(self, table_name, condition):
        """
        删除数据
        :param table_name: 表名
        :param condition: 删除条件，例如 "WHERE id = ?"
        """
        conn = self.db_pool.get_connection()
        try:
            cursor = conn.cursor()
            sql = f"DELETE FROM {table_name} {condition}"
            cursor.execute(sql)
            conn.commit()
        except Exception as e:
            logger.warning(f"删除数据失败：{str(e)}")
        finally:
            self.db_pool.release_connection(conn)

    def close_connection(self):
        """
        关闭数据库连接
        """
        self.db_pool.close_all()

# 示例使用
if __name__ == "__main__":
    db = SQLiteHelper("example.db")

    # 创建表
    db.create_table("users", {
        "id": "INTEGER PRIMARY KEY",
        "name": "TEXT",
        "age": "INTEGER"
    })

    # 插入数据
    db.insert_data("users", {"name": "Alice", "age": 25})
    db.insert_data("users", {"name": "Bob", "age": 30})
    db.insert_data("users", {"name": "Charlie", "age": 35})

    # 查询多条数据
    db.fetch_data("users")

    # 查询单条数据
    db.fetch_one("users", condition="WHERE name = 'Alice'")

    # 分页查询
    db.fetch_paginated_data("users", page=1, page_size=2)

    # 更新数据
    db.update_data("users", {"age": 40}, "WHERE name = 'Bob'")

    # 删除数据
    db.delete_data("users", "WHERE name = 'Charlie'")

    db.close_connection()