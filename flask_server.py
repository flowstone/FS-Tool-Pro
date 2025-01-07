from werkzeug.serving import make_server
import threading
from flask import Flask, render_template, request, send_from_directory
import os

from loguru import logger
from src.util.common_util import CommonUtil

# 全局变量定义
SAVE_DIR = CommonUtil.get_flask_mini_dir()
os.makedirs(SAVE_DIR, exist_ok=True)



# 存储上传的文本消息
uploaded_texts = []

# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    """检查文件类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def render_index_page(error=None):
    """渲染主页，避免重复代码，传递错误信息"""
    return render_template('index.html', files=os.listdir(SAVE_DIR), texts=uploaded_texts, error=error)


def create_app():
    """
    工厂函数，用于动态创建 Flask 应用实例。
    """
    app = Flask(__name__)

    @app.route('/')
    def index():
        return render_index_page()

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return render_index_page(error="No file part")

        file = request.files['file']

        if file.filename == '':
            return render_index_page(error="No selected file")

        secure_name = file.filename
        logger.info(f"安全处理后的文件名: {secure_name}")
        file_path = os.path.join(SAVE_DIR, secure_name)
        file.save(file_path)

        return render_index_page()

    @app.route('/send_text', methods=['POST'])
    def send_text():
        text = request.form['text']
        if text:
            uploaded_texts.append(text)
            return render_index_page()

        return render_index_page(error="Text cannot be empty!")

    @app.route('/files/<filename>')
    def uploaded_file(filename):
        return send_from_directory(SAVE_DIR, filename)

    return app

def run_flask():
    """启动 Flask 服务"""
    app = create_app()  # 动态创建 Flask 应用实例
    server = make_server("0.0.0.0", 5678, app)
    server.timeout = 1  # 设置超时时间，避免 handle_request 无限阻塞
    try:
        logger.info("Flask server starting on http://127.0.0.1:5678")
        server.serve_forever()  # 永久运行 Flask 服务
    except Exception as e:
        logger.error(f"Error in Flask service: {e}")

def start_flask_in_thread():
    """将 Flask 服务启动在单独的线程中"""
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True  # 设置为守护线程，主程序退出时线程也会退出
    flask_thread.start()
    return flask_thread
