from jinja2 import FileSystemLoader, ChoiceLoader
from werkzeug.serving import make_server
import threading
from flask import Flask, render_template, request, send_from_directory
import os

from loguru import logger
from src.util.common_util import CommonUtil

# 全局变量定义
# Flask 服务的基础目录
FLASK_DIR = CommonUtil.get_flask_mini_dir()
EXTERNAL_UPDATE_DIR = os.path.join(FLASK_DIR, "uploads")
EXTERNAL_TEMPLATES_DIR = os.path.join(FLASK_DIR, "pages")  # 假设外部文件夹位置
os.makedirs(EXTERNAL_UPDATE_DIR, exist_ok=True)
os.makedirs(EXTERNAL_TEMPLATES_DIR, exist_ok=True)



# 存储上传的文本消息
uploaded_texts = []
# 允许上传的文件类型
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# 全局变量存储动态路由和标题
dynamic_routes = []


def allowed_file(filename):
    """检查文件类型"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def render_index_page(error=None):
    """渲染主页，传递错误信息和动态路由信息"""
    return render_template(
        'index.html',
        files=os.listdir(EXTERNAL_UPDATE_DIR),
        texts=uploaded_texts,
        error=error,
        dynamic_routes=dynamic_routes
    )


def create_app():
    """
    工厂函数，用于动态创建 Flask 应用实例。
    """
    app = Flask(__name__)
    # 配置多个模板加载路径
    app.jinja_options = dict(
        loader=ChoiceLoader([
            FileSystemLoader(os.path.join(os.path.dirname(__file__), 'templates')),  # 默认模板目录
            FileSystemLoader(EXTERNAL_TEMPLATES_DIR)  # 外部模板目录
        ])
    )

    @app.route('/')
    def index():
        return render_index_page()

    @app.route('/upload', methods=['POST'])
    def upload_file():
        if 'file' not in request.files:
            return render_index_page(error="没有文件部分")

        file = request.files['file']

        if file.filename == '':
            return render_index_page(error="请选择文件")

        secure_name = file.filename
        logger.info(f"安全处理后的文件名: {secure_name}")
        file_path = os.path.join(EXTERNAL_UPDATE_DIR, secure_name)
        file.save(file_path)

        return render_index_page()

    @app.route('/send_text', methods=['POST'])
    def send_text():
        text = request.form['text']
        if text:
            uploaded_texts.append(text)
            return render_index_page()

        return render_index_page(error="请输入文本!")

    @app.route('/files/<filename>')
    def uploaded_file(filename):
        return send_from_directory(EXTERNAL_UPDATE_DIR, filename)

    # 动态创建路由
    def create_dynamic_routes():
        """
        动态创建路由，同时记录路由和对应 HTML 的标题。
        """
        for directory in [EXTERNAL_TEMPLATES_DIR]:
            for filename in os.listdir(directory):
                if filename.endswith('.html'):
                    route_name = filename.replace('.html', '')
                    route_path = f"/{route_name}"

                    # 从 HTML 文件中提取标题
                    html_file_path = os.path.join(directory, filename)
                    with open(html_file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    title = extract_html_title(content)

                    # 添加到动态路由列表
                    dynamic_routes.append({'route': route_path, 'title': title})

                    # 创建动态路由
                    @app.route(route_path)
                    def dynamic_route(route_name=route_name):
                        return render_template(f'{route_name}.html')



    create_dynamic_routes()
    return app

# 从 HTML 文件内容中提取标题标签内容。
def extract_html_title(content):
    """
    从 HTML 文件内容中提取标题标签内容。
    """
    import re
    match = re.search(r'<title>(.*?)</title>', content, re.IGNORECASE)
    return match.group(1) if match else 'No Title'

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
