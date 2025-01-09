from PySide6.QtCore import Qt
from PySide6.QtWidgets import QTextEdit, QSizePolicy


class TransparentTextBox(QTextEdit):
    """
    一个透明的文本框类，用于动态调整大小且不影响整体布局。
    """

    def __init__(self, placeholder_text="", parent=None):
        super().__init__(parent)

        # 设置为只读模式
        self.setReadOnly(True)

        # 设置透明背景
        self.setStyleSheet(
            "QTextEdit { background: transparent; border: none; font-size: 16px; color: gray; }"
        )

        # 设置占位文本
        self.setPlaceholderText(placeholder_text)

        # 设置拉伸策略
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # 禁用滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setMinimumHeight(10)  # 设置最小高度
