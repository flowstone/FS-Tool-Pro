from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QTextEdit, QSizePolicy


class TransparentTextBox(QTextEdit):
    """
    一个透明的文本框类，用于动态调整大小且布局紧凑。
    如果没有可用空间，高度为0；如果有可用空间，会自动填充空间。
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

        # 设置拉伸策略：水平扩展，高度优先填充剩余空间
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.MinimumExpanding)

        # 禁用滚动条
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # 固定宽度
        self.setFixedWidth(100)

    def sizeHint(self):
        """
        动态调整高度的推荐值。
        - 如果没有足够的拉伸空间，高度为 0。
        - 如果有拉伸空间，高度动态调整。
        """
        content_height = self.document().size().height()
        return QSize(self.width(), max(int(content_height), 0))

    def minimumSizeHint(self):
        """
        设置最小尺寸提示为 0，确保在没有拉伸空间时完全“消失”。
        """
        return QSize(self.width(), 0)
