class FsConstants:
    """
    ---------------------
    宽度为0 高度为0,则表示窗口【宽高】由组件们决定
    ---------------------
    """

    # 主窗口相关常量
    APP_WINDOW_WIDTH = 300
    APP_WINDOW_HEIGHT = 300
    APP_WINDOW_TITLE = "FS Tool Pro"
    VERSION = "0.2.7"
    COPYRIGHT_INFO = f"© 2025 {APP_WINDOW_TITLE}"


    # 悬浮球相关常量
    APP_MINI_SIZE = 80
    APP_MINI_WINDOW_TITLE = ""

    # 工具栏相关常量
    TOOLBAR_HELP_TITLE = "帮助"
    TOOLBAR_README_TITLE = "说明"
    TOOLBAR_AUTHOR_TITLE = "作者"

    # 主界面APP列表名
    APP_TITLE_DESKTOP_CLOCK = "透明时间"
    APP_TITLE_STICK_NOTE = "快捷便签"
    APP_TITLE_PASSWORD_GENERATOR = "密码生成器"
    APP_TITLE_RSA_GENERATOR = "RSA生成器"
    APP_TITLE_GENERATOR_TOOL = "生成器工具"
    APP_TITLE_RENAMER_TOOL = "重命名工具"
    APP_TITLE_IMAGE_TOOL = "图片工具"
    APP_TITLE_FILE_TOOL = "文件工具"
    APP_TITLE_CREATE_FOLDER = "创建文件夹"
    APP_TITLE_HASH_CALCULATOR = "HASH校验"
    APP_TITLE_IP_TOOL = "网络工具"
    APP_TITLE_APP_SIGNER = "文件签名"
    APP_TITLE_FAST_SENDER_TOOL = "快速发送"
    APP_TITLE_COLOR_PICKER = "取色器"

    WINDOW_TITLE_DESKTOP_CLOCK = "透明时间"
    WINDOW_TITLE_STICK_NOTE = "快捷便签"
    WINDOW_TITLE_GENERATOR_TOOL = "生成器工具"
    WINDOW_TITLE_PASSWORD_GENERATOR = "密码生成器"
    WINDOW_TITLE_PERSON_PASSWORD_GENERATOR = "个性密码生成器"
    WINDOW_TITLE_RSA_GENERATOR = "RSA生成器"
    WINDOW_TITLE_RENAME_TOOL = "重命名工具"
    WINDOW_TITLE_RENAME_GENERATE = "重命名生成"
    WINDOW_TITLE_RENAME_REPLACE = "重命名替换"
    WINDOW_TITLE_IMAGE_TOOL = "图片工具"
    WINDOW_TITLE_IMAGE_CONVERT = "图片转换"
    WINDOW_TITLE_IMAGE_HEIC_JPG = "批量HEIC转JPG"
    WINDOW_TITLE_INVISIBLE_WATERMARK = "图片隐水印"
    WINDOW_TITLE_FILE_TOOL = "文件工具"
    WINDOW_TITLE_FILE_GENERATOR = "文件批量生成"
    WINDOW_TITLE_FILE_COMPARATOR = "文件比较"
    WINDOW_TITLE_FILE_ENCRYPTOR = "文件批量加密"
    WINDOW_TITLE_CREATE_FOLDER = "创建文件夹"
    WINDOW_TITLE_MOVE_FILE = "移动文件"
    WINDOW_TITLE_HASH_CALCULATOR = "HASH校验"
    WINDOW_TITLE_IP_INFO_TOOL = "网络工具"
    WINDOW_TITLE_IP_INFO = "网络信息"
    WINDOW_TITLE_IP_INFO_PORT_SCANNER = "端口扫描"
    WINDOW_TITLE_IP_INFO_PORT_KILLER = "关闭端口"
    WINDOW_TITLE_APP_SIGNER_TOOL = "文件签名工具"
    WINDOW_TITLE_APP_SIGNER = "文件签名"
    WINDOW_TITLE_APP_SIGNER_GENERATE_CERTIFICATE = "证书生成"
    WINDOW_TITLE_APP_SIGNER_PUBLIC_KEY_EXTRACTOR = "证书转换"
    WINDOW_TITLE_FAST_SENDER_TOOL = "局域网文件传输"
    WINDOW_TITLE_FAST_SENDER = "局域网文件传输"
    WINDOW_TITLE_FAST_SENDER_MINI = "Flask Mini 服务"
    WINDOW_TITLE_WEBDAV_SERVER = "WebDAV服务"
    WINDOW_TITLE_COLOR_PICKER = "图片取色器"




    # 桌面时钟相关常量
    DESKTOP_CLOCK_WINDOW_WIDTH = 0
    DESKTOP_CLOCK_WINDOW_HEIGHT = 0

    # 批量创建文件夹相关常量
    CREATE_FOLDER_WINDOW_WIDTH = 0
    CREATE_FOLDER_WINDOW_HEIGHT = 0

    # 批量修改文件名相关常量
    FILE_RENAMER_WINDOW_WIDTH = 0
    FILE_RENAMER_WINDOW_HEIGHT = 0
    FILE_RENAMER_TYPE_FILE = "文件"
    FILE_RENAMER_TYPE_FOLDER = "文件夹"

    # 批量HEIC转JPG
    HEIC_JPG_WINDOW_WIDTH = 0
    HEIC_JPG_WINDOW_HEIGHT = 0
    HEIC_JPG_WINDOW_TITLE = "批量HEIC转JPG(递归)"

    # 图片转换相关常量
    PIC_CONVERSION_WINDOW_WIDTH = 500
    PIC_CONVERSION_WINDOW_HEIGHT = 400


    #快捷便签相关常量
    STICK_NOTE_WINDOW_WIDTH = 400
    STICK_NOTE_WINDOW_HEIGHT = 300
    STICK_NOTE_WINDOW_MIN_WIDTH = 300
    STICK_NOTE_WINDOW_MIN_HEIGHT = 200



    # 共用的常量，应用图标
    APP_ICON_FULL_PATH = "resources/images/app.ico"
    APP_MINI_ICON_FULL_PATH = "resources/images/app_mini.ico"
    APP_BAR_ICON_FULL_PATH = "resources/images/app_bar.ico"
    AUTHOR_MAIL = "xueyao.me@gmail.com"
    AUTHOR_BLOG = "https://blog.xueyao.tech"
    AUTHOR_GITHUB = "https://github.com/flowstone"
    PROJECT_ADDRESS = "https://github.com/flowstone/FS-Tool-Pro"
    BASE_QSS_PATH = "resources/qss/base.qss"
    BASE_COLOR_MAP = "resources/images/img_colormap.gif"
    LICENSE_FILE_PATH = "resources/txt/LICENSE"

    APP_ICON_RESOURCE_PATH = "resources/images/icon/"
    APP_ICON_DESKTOP_CLOCK = "desktop_clock_icon.svg"
    APP_ICON_STICK_NOTE = "stick_note_icon.svg"
    APP_ICON_PASSWORD_GENERATOR = "password_generator_icon.svg"
    APP_ICON_RSA_GENERATOR = "rsa_generator_icon.svg"
    APP_ICON_GENERATOR_TOOL = "rsa_generator_icon.svg"
    APP_ICON_RENAMER_TOOL = "renamer_tool_icon.svg"
    APP_ICON_IMAGE_TOOL = "image_tool_icon.svg"
    APP_ICON_FILE_TOOL = "file_tool_icon.svg"
    APP_ICON_CREATE_FOLDER = "create_folder_icon.svg"
    APP_ICON_HASH_CALCULATOR = "hash_calculator_icon.svg"
    APP_ICON_IP_TOOL = "ip_tool_icon.svg"
    APP_ICON_APP_SIGNER = "app_signer_icon.svg"
    APP_ICON_FAST_SENDER_TOOL = "fast_sender_icon.svg"
    APP_ICON_COLOR_PICKER = "color_picker_icon.svg"



    BUTTON_IMAGE_LOCK_OPEN = "resources/btn/lock-open-solid.svg"
    BUTTON_IMAGE_LOCK_CLOSE = "resources/btn/lock-solid.svg"

    # 保存文件路径
    SAVE_FILE_PATH_WIN = "C:\\FS-Tool-Pro\\"
    SAVE_FILE_PATH_MAC = "~/FS-Tool-Pro/"
    EXTERNAL_DATABASE_FILE = "fs-tool-pro.db"
    EXTERNAL_FAST_SENDER_DIR = "fs_received_files"
    EXTERNAL_FLASK_MINI_DIR = "fs_flask_web"
    EXTERNAL_APP_INI_FILE = "app.ini"

    APP_INI_FILE = "app.ini"
    HELP_PDF_FILE_PATH = "resources/pdf/help.pdf"
    FONT_FILE_PATH = "resources/fonts/AlimamaFangYuanTiVF-Thin.ttf"

    #首选项
    PREFERENCES_WINDOW_TITLE = "首选项"
    PREFERENCES_WINDOW_TITLE_ABOUT = "关于"
    PREFERENCES_WINDOW_TITLE_GENERAL = "常规"
