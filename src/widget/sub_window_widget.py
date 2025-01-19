from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget


class SubWindowWidget(QWidget):
    closed_signal = Signal()

    def __init__(self):
        super().__init__()

    #重写关闭事件
    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)