import sys

from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QMessageBox, QHBoxLayout
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, Signal
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
from src.util.message_util import MessageUtil
from src.widget.hover_image_button import HoverImageButton
from loguru import logger

class StickyNoteApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  Signal()
    def __init__(self):
        super().__init__()
        # 标记窗口当前是否可操作（初始设为可操作）
        self.is_operable = True
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_STICK_NOTE} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_STICK_NOTE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setWindowOpacity(0.95)  # 设置为更加透明的效果
        self.text_edit = QTextEdit(self)
        self.text_edit.setPlaceholderText("请输入便签内容...")
        self.text_edit.setStyleSheet("""
            QTextEdit {
                border-radius: 5px;
                padding: 10px;
            }
            QTextEdit::verticalScrollBar {
                width: 10px;
                border-radius: 5px;
            }
            QTextEdit::verticalScrollBar::handle {
                border-radius: 5px;
                min-height: 20px;
            }
            QTextEdit::verticalScrollBar::add-line, QTextEdit::verticalScrollBar::sub-line {
                height: 0px;
                subcontrol-position: bottom;
                subcontrol-origin: margin;
            }
        """)

        self.save_button = QPushButton('保存', self)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_note)

        self.clear_button = QPushButton('清空', self)
        self.clear_button.setObjectName("exit_button")
        self.clear_button.setToolTip('点击清空便签中的内容')
        self.clear_button.clicked.connect(self.clear_text)

        self.save_button.setShortcut('Ctrl+S')  # 保存快捷键
        self.clear_button.setShortcut('Ctrl+L')  # 清空快捷键

        # 创建切换状态的按钮
        lock_button = HoverImageButton(FsConstants.BUTTON_IMAGE_LOCK_OPEN, FsConstants.BUTTON_IMAGE_LOCK_CLOSE)

        lock_button.clicked.connect(self.toggle_window_state)

        # 创建水平布局放置两个按钮
        button_layout = QHBoxLayout()
        button_layout.addWidget(lock_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.clear_button)

        layout = QVBoxLayout()
        layout.addWidget(self.text_edit)
        layout.addLayout(button_layout)
        layout.setContentsMargins(20, 20, 20, 20)

        self.setLayout(layout)
        self.setGeometry(0, 0, FsConstants.STICK_NOTE_WINDOW_WIDTH, FsConstants.STICK_NOTE_WINDOW_HEIGHT)
        #self.resize(FsConstants.STICK_NOTE_WINDOW_WIDTH, FsConstants.STICK_NOTE_WINDOW_HEIGHT)
        self.setMinimumSize(FsConstants.STICK_NOTE_WINDOW_MIN_WIDTH, FsConstants.STICK_NOTE_WINDOW_MIN_HEIGHT)


    def toggle_window_state(self):
        """
        点击按钮切换窗口可操作状态
        """
        self.is_operable = not self.is_operable
        if self.is_operable:
            self.clear_button.setEnabled(True)
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowType.WindowStaysOnTopHint)
        else:
            self.clear_button.setEnabled(False)
            self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.show()

    def closeEvent(self, event):
        """
        重写关闭事件，根据状态决定是否响应
        """
        if self.is_operable:
            event.accept()
            # 在关闭事件中发出信号
            self.closed_signal.emit()
        else:
            event.ignore()

    def save_note(self):
        note_text = self.text_edit.toPlainText().strip()
        if note_text:
            logger.info(f'保存便签内容: {note_text}')
            MessageUtil.show_success_message('便签内容已成功保存！')
        else:
            MessageUtil.show_warning_message('请输入便签内容后再保存哦！')

    def clear_text(self):
        self.text_edit.clear()
        MessageUtil.show_success_message('便签内容已清空。')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = StickyNoteApp()
    window.show()
    sys.exit(app.exec())