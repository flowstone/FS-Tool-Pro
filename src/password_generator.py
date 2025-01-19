import sys
import random
import string
import pyperclip

from PySide6.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QCheckBox, QPushButton, QVBoxLayout, QHBoxLayout, QSpinBox
)

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from loguru import logger
from PySide6.QtCore import QThread, Signal

from src.widget.sub_window_widget import SubWindowWidget
from src.widget.transparent_textbox_widget import TransparentTextBox


class PasswordGeneratorThread(QThread):
    password_generated = Signal(str)

    def __init__(self, main_char_pool, special_char_pool, password_length, exclude_chars):
        super().__init__()
        self.main_char_pool = main_char_pool
        self.special_char_pool = special_char_pool
        self.password_length = password_length
        self.exclude_chars = exclude_chars

    def run(self):
        # 去除排除字符后的字符池
        main_char_pool = ''.join(c for c in self.main_char_pool if c not in self.exclude_chars)
        special_char_pool = ''.join(c for c in self.special_char_pool if c not in self.exclude_chars)

        if not main_char_pool and not special_char_pool:
            self.password_generated.emit("字符池为空，请检查排除字符或选择字符类型")
            return

        special_char_count = min(max(self.password_length // 10, 4), len(special_char_pool))
        main_char_count = self.password_length - special_char_count

        if not main_char_pool:
            self.password_generated.emit("主字符池为空，请检查排除字符")
            return

        password = (
            ''.join(random.choice(main_char_pool) for _ in range(main_char_count)) +
            ''.join(random.choice(special_char_pool) for _ in range(special_char_count))
        )

        password = ''.join(random.sample(password, len(password)))  # 打乱密码
        self.password_generated.emit(password)

class PasswordGeneratorApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_PASSWORD_GENERATOR} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_PASSWORD_GENERATOR)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        # 初始化界面元素
        title_label = QLabel("密码生成器")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        
        self.label = QLabel("生成的密码:")
        self.generated_password = QLineEdit(self)
        self.generated_password.setReadOnly(True)
        # 复制按钮
        self.copy_button = QPushButton("复制", self)
        self.copy_button.clicked.connect(self.copy_password)

        self.exclude_label = QLabel("排除字符:")
        self.exclude_input = QLineEdit(self)
        self.exclude_input.setText("0oO1iIlLq9g")

        self.include_digits = QCheckBox("包含数字")
        self.include_lowercase = QCheckBox("包含小写字母")
        self.include_uppercase = QCheckBox("包含大写字母")
        self.include_special = QCheckBox("包含特殊字符")

        self.include_digits.setChecked(True)
        self.include_lowercase.setChecked(True)
        self.include_uppercase.setChecked(True)

        self.length_label = QLabel("密码长度:")
        self.password_length_input = QSpinBox(self)
        self.password_length_input.setRange(4, 64)
        self.password_length_input.setValue(16)

        self.generate_button = QPushButton("生成密码", self)
        self.generate_button.clicked.connect(self.start_password_generation)

        layout = QVBoxLayout()

        layout.addWidget(title_label)
        options_layout = QHBoxLayout()
        options_layout.addWidget(self.include_digits)
        options_layout.addWidget(self.include_lowercase)
        options_layout.addWidget(self.include_uppercase)
        options_layout.addWidget(self.include_special)

        layout.addLayout(options_layout)
        layout.addWidget(self.exclude_label)
        layout.addWidget(self.exclude_input)
        layout.addWidget(self.length_label)
        layout.addWidget(self.password_length_input)
        layout.addWidget(self.generate_button)
        layout.addWidget(self.label)
        # 新的水平布局，将生成的密码和复制按钮放在同一行
        password_display_layout = QHBoxLayout()
        password_display_layout.addWidget(self.generated_password)
        password_display_layout.addWidget(self.copy_button)
        layout.addLayout(password_display_layout)
        layout.addWidget(TransparentTextBox())
        self.setLayout(layout)

    def start_password_generation(self):
        # 获取输入的数据并开始生成密码
        exclude_chars = self.exclude_input.text()

        main_char_pool = ""
        special_char_pool = ""
        if self.include_digits.isChecked():
            main_char_pool += string.digits
        if self.include_lowercase.isChecked():
            main_char_pool += string.ascii_lowercase
        if self.include_uppercase.isChecked():
            main_char_pool += string.ascii_uppercase
        if self.include_special.isChecked():
            special_char_pool += string.punctuation

        password_length = self.password_length_input.value()

        # 创建并启动线程来生成密码
        self.password_thread = PasswordGeneratorThread(main_char_pool, special_char_pool, password_length, exclude_chars)
        self.password_thread.password_generated.connect(self.display_generated_password)
        self.password_thread.start()

    def display_generated_password(self, password):
        # 显示生成的密码
        self.generated_password.setText(password)


    def copy_password(self):
        password = self.generated_password.text()
        if password:
            pyperclip.copy(password)
            self.generated_password.selectAll()  # 全选文本框中的文本

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PasswordGeneratorApp()
    window.show()
    sys.exit(app.exec())
