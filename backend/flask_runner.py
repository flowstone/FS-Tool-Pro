# backend/flask_runner.py
from werkzeug.serving import make_server
from backend.flask_server import create_app, shutdown_event
from multiprocessing import Queue
from loguru import logger


def run_flask(queue: Queue):
    """启动 Flask 服务并通过队列传递状态信息"""
    app = create_app()  # 动态创建 Flask 应用实例
    server = make_server("0.0.0.0", 5678, app)
    server.timeout = 1  # 设置超时时间，避免 handle_request 无限阻塞

    queue.put("Flask service started")  # 通知主进程服务已启动
    try:
        while not shutdown_event.is_set():
            try:
                server.handle_request()
            except Exception as e:
                logger.error(f"Error in Flask service: {e}")
                queue.put(f"Error: {e}")  # 将错误发送到主进程
    finally:
        server.shutdown()
        queue.put("Flask service stopped")  # 通知主进程服务已停止
