from PySide6.QtGui import QColor, QFont


def create_font(size: int, bold: bool = False, weight = QFont.Weight.Normal, italic: bool = False) -> QFont:
    """动态生成字体"""
    font = QFont()
    font.setPointSize(size)
    font.setBold(bold)
    font.setWeight(weight)
    font.setItalic(italic)
    return font

class FontConstants:

    # 预定义字体常量
    H1 = create_font(32, bold=True, weight=QFont.Weight.Bold)
    H2 = create_font(28, bold=True, weight=QFont.Weight.DemiBold)
    H3 = create_font(24, bold=True, weight=QFont.Weight.Medium)
    BODY_LARGE = create_font(18)
    BODY_NORMAL = create_font(16)
    BODY_SMALL = create_font(14)

    # 斜体字体
    ITALIC_LARGE = create_font(18, italic=True)
    ITALIC_NORMAL = create_font(16, italic=True)
    ITALIC_SMALL = create_font(14, italic=True)

    # 粗体字体
    BOLD_LARGE = create_font(18, bold=True, weight=QFont.Weight.Bold)
    BOLD_NORMAL = create_font(16, bold=True, weight=QFont.Weight.Bold)
    BOLD_SMALL = create_font(14, bold=True, weight=QFont.Weight.Bold)