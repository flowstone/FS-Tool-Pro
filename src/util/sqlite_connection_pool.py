import sqlite3
import threading
from queue import Queue, Empty


class SQLiteConnectionPool:
    """
    自定义 SQLite 连接池类
    """
    def __init__(self, database, pool_size=5):
        self.database = database
        self.pool_size = pool_size
        self.pool = Queue(maxsize=pool_size)
        self.lock = threading.Lock()

        # 初始化连接池
        for _ in range(pool_size):
            conn = sqlite3.connect(self.database, check_same_thread=False)
            self.pool.put(conn)

    def get_connection(self):
        """
        获取一个可用的 SQLite 连接
        """
        try:
            return self.pool.get(timeout=5)  # 等待连接可用
        except Empty:
            raise Exception("连接池耗尽，没有可用连接！")

    def release_connection(self, conn):
        """
        释放连接回连接池
        """
        with self.lock:
            self.pool.put(conn)

    def close_all(self):
        """
        关闭所有连接
        """
        while not self.pool.empty():
            conn = self.pool.get_nowait()
            conn.close()
