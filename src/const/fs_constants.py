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

    # 悬浮球相关常量
    APP_MINI_WINDOW_WIDTH = 90
    APP_MINI_WINDOW_HEIGHT = 90
    APP_MINI_WINDOW_TITLE = ""

    # 工具栏相关常量
    TOOLBAR_HELP_TITLE = "帮助"
    TOOLBAR_README_TITLE = "说明"
    TOOLBAR_AUTHOR_TITLE = "作者"

    DESKTOP_CLOCK_WINDOW_TITLE = "透明时间"
    CREATE_FOLDER_WINDOW_TITLE = "创建文件夹"
    FILE_RENAMER_WINDOW_TITLE = "重命名使者"
    HEIC_JPG_BUTTON_TITLE = "HEIC作家"
    PIC_CONVERSION_WINDOW_TITLE = "图转大师"
    AUTO_ANSWERS_WINDOW_TITLE = "自动答题"
    STICK_NOTE_WINDOW_TITLE = "快捷便签"
    PASSWORD_GENERATOR_TITLE = "密码生成器"
    FILE_GENERATOR_WINDOW_TITLE = "文件生成"
    FILE_COMPARATOR_WINDOW_TITLE = "文件比较"
    FILE_ENCRYPTOR_WINDOW_TITLE = "文件加密"
    RSA_KEY_GENERATOR_WINDOW_TITLE = "RSA生成器"
    HASH_CALCULATOR_WINDOW_TITLE = "HASH校验"

    NETWORK_TOOL_WINDOW_TITLE = "网络工具"
    PORT_SCANNER_WINDOW_TITLE = "端口扫描器"
    PORT_KILLER_WINDOW_TITLE = "端口杀手"
    IP_TOOL_WINDOW_TITLE = "IP信息"
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

    # 自动答题相关常量
    AUTO_ANSWERS_WINDOW_WIDTH = 0
    AUTO_ANSWERS_WINDOW_HEIGHT = 0
    AUTO_ANSWERS_TITLE_IMAGE = "resources/images/auto_answers_title.png"
    AUTO_ANSWERS_PASSWORD_MD5 = "adf0558822da93b55f6fc48790ff3137"
    AUTO_ANSWERS_DRIVER_PATH = "resources/driver"
    AUTO_ANSWERS_WIN_DRIVER_NAME = "chromedriver.exe"
    AUTO_ANSWERS_OTHER_DRIVER_NAME = "chromedriver"

    #快捷便签相关常量
    STICK_NOTE_WINDOW_WIDTH = 400
    STICK_NOTE_WINDOW_HEIGHT = 300
    STICK_NOTE_WINDOW_MIN_WIDTH = 300
    STICK_NOTE_WINDOW_MIN_HEIGHT = 200

    #密码生成器

    # 颜色相关常量
    BACKGROUND_COLOR = "#f0f0f0"
    BUTTON_COLOR_NORMAL = "#3498db"
    BUTTON_COLOR_HOVER = "#2980b9"
    BUTTON_COLOR_PRESS = "#1f618d"

    # 字体相关常量
    DEFAULT_FONT_FAMILY = "Arial"
    DEFAULT_FONT_SIZE = 12

    # 共用的常量，应用图标
    APP_ICON_PATH = "resources/images/app.ico"
    APP_MINI_ICON_PATH = "resources/images/app_mini.ico"
    LOADING_PATH = "resources/images/loading.gif"
    AUTHOR_MAIL = "xueyao.me@gmail.com"
    AUTHOR_BLOG = "https://blog.xueyao.tech"
    AUTHOR_GITHUB = "https://github.com/flowstone"
    PROJECT_ADDRESS = "https://github.com/flowstone/FS-Tool"
    BASE_QSS_PATH = "resources/qss/base.qss"
    BASE_COLOR_MAP = "resources/images/img_colormap.gif"

    BUTTON_ICON_PATH = "resources/images/icon/"
    BUTTON_TIME_ICON = "time-icon.svg"
    BUTTON_PIC_ICON = "img_conv-icon.svg"
    BUTTON_FOLDER_ICON = "folder-icon.svg"
    BUTTON_FILE_ICON = "move-icon.svg"
    BUTTON_HEIC_ICON = "heic_jpg-icon.svg"
    BUTTON_ANSWERS_ICON = "auto_answers-icon.svg"
    BUTTON_PASSWORD_ICON = "unlock-icon.svg"
    BUTTON_STICK_NOTE_ICON = "business-icon.svg"
    BUTTON_FILE_GENERATOR_ICON = "file_generator-icon.svg"
    BUTTON_FILE_COMPARATOR_ICON = "file_comparator-icon.svg"
    BUTTON_FILE_ENCRYPTOR_ICON = "file_encryptor-icon.svg"
    BUTTON_RSA_KEY_GENERATOR_ICON = "rsa-icon.svg"
    BUTTON_HASH_CALCULATOR_ICON = "MD5-icon.svg"
    BUTTON_PORT_SCANNER_ICON = "port-scanner-icon.svg"
    BUTTON_PORT_KILLER_ICON = "port-killer-icon.svg"
    BUTTON_NETWORK_TOOL_ICON = "network-tool-icon.svg"


    BUTTON_IMAGE_LOCK_OPEN = "resources/btn/lock-open-solid.svg"
    BUTTON_IMAGE_LOCK_CLOSE = "resources/btn/lock-solid.svg"

    # 保存文件路径
    SAVE_FILE_PATH_WIN = "C:\\"
    SAVE_FILE_PATH_MAC = "~"
    DATABASE_FILE = "database.db"
    AUTO_ANSWERS_TABLE_NAME = "auto_answers_log"

    APP_CONFIG_FILE = "config.json"
    HELP_PDF_FILE_PATH = "resources/pdf/help.pdf"
    FONT_FILE_PATH = "resources/fonts/AlimamaFangYuanTiVF-Thin.ttf"