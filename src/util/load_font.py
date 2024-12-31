from PyQt5.QtGui import QFontDatabase
from loguru import logger
# 加载外部字体
def load_external_font(font_path):
    font_id = QFontDatabase.addApplicationFont(font_path)
    if font_id == -1:
        logger.warning("字体加载失败")
    else:
        logger.info("字体加载成功")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        return font_family