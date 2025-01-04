from PyQt6.QtWidgets import QProgressBar
from PyQt6.QtCore import Qt


class CustomProgressBar(QProgressBar):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setValue(0)
        self.setMinimum(0)
        self.setMaximum(100)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QProgressBar {
                border-radius: 5px;
                text-align: center;
                font-size: 14px;
                color: black;
            }
            QProgressBar::chunk {
                border-radius: 5px;
                background-color: #00cc66;
                font-size: 14px;
                width: 10px;
                margin: 1px;
            }
        """)

    def reset_progress(self):
        """
        重置进度条为初始状态
        """
        self.setValue(0)
    def set_range(self, min_value, max_value):
        """设置进度条的范围"""
        self.setRange(min_value, max_value)

    def update_progress(self, value):
        """
        更新进度条值
        :param value: 整数，进度值 (0-100)
        """
        self.setValue(value)
        if value < 50:
            self.setStyleSheet("""
                QProgressBar::chunk {
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #ff6666;  /* 红色 */
                }
            """)
        elif value < 80:
            self.setStyleSheet("""
                QProgressBar::chunk {
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #ffcc00;  /* 黄色 */
                }
            """)
        else:
            self.setStyleSheet("""
                QProgressBar::chunk {
                    border-radius: 5px;
                    font-size: 14px;
                    background-color: #00cc66;  /* 绿色 */
                }
            """)