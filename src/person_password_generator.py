import sys
import hashlib
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QCheckBox, QLabel, QGroupBox, QScrollArea
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QClipboard, QIcon
from loguru import logger

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class PersonPasswordGeneratorApp(SubWindowWidget):
    def __init__(self):
        super().__init__()
        self.substitution_rules = {
            'a': '@', 's': '$', 'o': '0',
            'e': '3', 'i': '!', 'g': '9',
            'b': '8', 'l': '1', 't': '7'
        }
        self.second_substitution = {
            '@': '^', '$': '§', '0': '°',
            '3': '€', '!': '¡', '9': '⑨'
        }
        self.init_ui()


    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_PERSON_PASSWORD_GENERATOR} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_PERSON_PASSWORD_GENERATOR)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 输入区域
        input_group = QGroupBox("输入参数")
        self.base_pw = QLineEdit()
        self.base_pw.setPlaceholderText("输入基础密码")
        self.site_feature = QLineEdit()
        self.site_feature.setPlaceholderText("输入网站特征（2位以上）")
        self.secret_key = QLineEdit()
        self.secret_key.setPlaceholderText("输入个人密钥（2位以上）")

        # 规则分组
        rule_scroll = QScrollArea()
        rule_group = QGroupBox("加密规则（至少选择3项）")
        rule_layout = QVBoxLayout()

        # 规则复选框
        self.dynamic_salt = QCheckBox("动态盐值组合")
        self.char_sub = QCheckBox("基础字符替换（a→@）")
        self.double_sub = QCheckBox("高级符号替换（@→^）")
        self.vowel_upper = QCheckBox("元音字母大写")
        self.pos_swap = QCheckBox("奇偶位交换")
        self.keyboard_shift = QCheckBox("键盘右移（全字符）")
        self.insert_separator = QCheckBox("插入分隔符（每4位）")
        self.ascii_shift = QCheckBox("ASCII码+5（循环）")
        self.prime_transform = QCheckBox("质数位置大写")

        # 分组布局
        char_group = QGroupBox("字符处理")
        char_layout = QVBoxLayout()
        char_layout.addWidget(self.char_sub)
        char_layout.addWidget(self.double_sub)
        char_layout.addWidget(self.vowel_upper)
        char_group.setLayout(char_layout)

        pos_group = QGroupBox("位置变换")
        pos_layout = QVBoxLayout()
        pos_layout.addWidget(self.pos_swap)
        pos_layout.addWidget(self.keyboard_shift)
        pos_layout.addWidget(self.insert_separator)
        pos_group.setLayout(pos_layout)

        math_group = QGroupBox("数学变换")
        math_layout = QVBoxLayout()
        math_layout.addWidget(self.ascii_shift)
        math_layout.addWidget(self.prime_transform)
        math_group.setLayout(math_layout)

        # 主规则布局
        rule_layout.addWidget(self.dynamic_salt)
        rule_layout.addWidget(char_group)
        rule_layout.addWidget(pos_group)
        rule_layout.addWidget(math_group)
        rule_group.setLayout(rule_layout)
        rule_scroll.setWidget(rule_group)
        rule_scroll.setWidgetResizable(True)

        # 结果区域
        self.result = QLineEdit()
        self.result.setReadOnly(True)
        self.copy_btn = QPushButton("复制到剪贴板")
        self.generate_btn = QPushButton("生成密码")

        # 布局设置
        main_layout = QVBoxLayout()
        input_layout = QVBoxLayout()
        input_layout.addWidget(self.base_pw)
        input_layout.addWidget(self.site_feature)
        input_layout.addWidget(self.secret_key)
        input_group.setLayout(input_layout)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.generate_btn)
        btn_layout.addWidget(self.copy_btn)

        main_layout.addWidget(input_group)
        main_layout.addWidget(rule_scroll)
        main_layout.addWidget(self.result)
        main_layout.addLayout(btn_layout)

        self.setLayout(main_layout)

        # 信号连接
        self.generate_btn.clicked.connect(self.generate_password)
        self.copy_btn.clicked.connect(self.copy_to_clipboard)

    def validate_inputs(self):
        """
        验证输入
        :return:
        """
        errors = []
        if not self.base_pw.text().strip():
            errors.append("基础密码不能为空")
        if len(self.site_feature.text()) < 2:
            errors.append("网站特征需要至少2个字符")
        if len(self.secret_key.text()) < 2:
            errors.append("个人密钥需要至少2个字符")

        selected_rules = sum([
            self.dynamic_salt.isChecked(),
            self.char_sub.isChecked(),
            self.double_sub.isChecked(),
            self.vowel_upper.isChecked(),
            self.pos_swap.isChecked(),
            self.keyboard_shift.isChecked(),
            self.insert_separator.isChecked(),
            self.ascii_shift.isChecked(),
            self.prime_transform.isChecked()
        ])
        if selected_rules < 3:
            errors.append("至少选择3项加密规则")

        if errors:
            self.show_error(" | ".join(errors))
            return False
        return True

    # 截取前16位Hash值
    @staticmethod
    def process_hash_salt(secret):
        """
        取前16位哈希盐值
        :param secret: 基础密码+网址特征+个人密钥
        :return: 截取前16位
        """
        hash_obj = hashlib.sha256(secret.encode()).hexdigest()
        return hash_obj[:16]

    # 截取16位Hash值
    @staticmethod
    def dynamic_salt_hash_salt(secret_part, final_combined_hash_digest):
        """
        动态盐值组合
        :param secret_part:str, 个人密钥
        :param final_combined_hash_digest:str, 最终组合Hash值
        :return: 截取的16位Hash值
        """
        if secret_part.isdigit():
            # 对密钥进行哈希
            secret_part_hash = hashlib.sha256(secret_part.encode()).hexdigest()
            start_index = 0
            for char in secret_part_hash:
                if char.isdigit():
                    start_index = int(char)
                    break
            if start_index + 16 <= len(final_combined_hash_digest):
                password = final_combined_hash_digest[start_index: start_index + 16]
            else:
                remaining_length = 16 - (len(final_combined_hash_digest) - start_index)
                password = final_combined_hash_digest[start_index:] + final_combined_hash_digest[:remaining_length]
        else:
            password = final_combined_hash_digest[:16]
        return password


    def apply_rules(self, password):
        site_part = self.site_feature.text().lower()
        secret_part = self.secret_key.text()
        # 动态盐值处理
        if self.dynamic_salt.isChecked():
            combined_for_pseudo_key = password + site_part
            pseudo_key = hashlib.sha256(combined_for_pseudo_key.encode()).hexdigest()
            final_combined = pseudo_key + secret_part
            final_combined_hash_digest = hashlib.sha256(final_combined.encode()).hexdigest()
            password = self.dynamic_salt_hash_salt(secret_part, final_combined_hash_digest)
        else:
            password += f"{site_part}{secret_part}"
            password = self.process_hash_salt(password)

        # 规则处理流程
        rules = [
            self.process_char_substitution,
            self.process_double_sub,
            self.process_vowel_upper,
            self.process_pos_swap,
            self.process_keyboard_shift,
            self.process_separator,
            self.process_ascii_shift,
            self.process_prime_transform
        ]

        for rule in rules:
            password = rule(password)

        return self.normalize_length(password)

    def process_char_substitution(self, password):
        """
        基础字符替换（a→@）
        :param password: str, 16位Hash值
        :return:
        """
        if self.char_sub.isChecked():
            return ''.join([self.substitution_rules.get(c.lower(), c) for c in password])
        return password

    def process_double_sub(self, password):
        """
        高级符号替换（@→^）
        :param password:  str, 16位Hash值
        :return:
        """
        if self.double_sub.isChecked():
            return ''.join([self.second_substitution.get(c, c) for c in password])
        return password

    def process_vowel_upper(self, password):
        """
        元音字母大写
        :param password:   str, 16位Hash值
        :return:
        """
        if self.vowel_upper.isChecked():
            return ''.join([c.upper() if c.lower() in 'aeiou' else c for c in password])
        return password

    def process_prime_transform(self, password):
        """
        质数位置大写
        :param password: str, 16位Hash值
        :return:
        """
        if self.prime_transform.isChecked():
            # 修改后的质数索引（0-based）
            primes = [1, 2, 4, 6, 10, 12, 16, 18]  # 对应第2、3、5、7、11、13、17、19位
            pwd_list = list(password)
            for i in primes:
                if i < len(pwd_list):
                    pwd_list[i] = pwd_list[i].upper()
            return ''.join(pwd_list)
        return password

    def process_pos_swap(self, password):
        """
        奇偶位交换
        :param password: str, 16位Hash值
        :return:
        """
        if self.pos_swap.isChecked():
            pwd_list = list(password)
            for i in range(0, len(pwd_list)-1, 2):
                pwd_list[i], pwd_list[i+1] = pwd_list[i+1], pwd_list[i]
            return ''.join(pwd_list)
        return password

    def process_keyboard_shift(self, password):
        """
        键盘右移（全字符）
        :param password: str, 16位Hash值
        :return:
        """
        if self.keyboard_shift.isChecked():
            keyboard_map = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM"
            shifted = "234567890wertyuiopasdfghjklzxcvbnmqQWERTYUIOPASDFGHJKLZXCVBNM1"
            return password.translate(str.maketrans(keyboard_map, shifted))
        return password

    def process_ascii_shift(self, password):
        """
        ASCII码+5（循环）
        :param password: str, 16位Hash值
        :return:
        """
        if self.ascii_shift.isChecked():
            shifted = []
            for c in password:
                new_ord = ord(c) + 5
                if new_ord > 126:
                    new_ord = 33 + (new_ord - 127)
                shifted.append(chr(new_ord))
            return ''.join(shifted)
        return password

    def process_separator(self, password):
        """
        插入分隔符（每4位）
        :param password: str, 16位Hash值
        :return:
        """
        if self.insert_separator.isChecked():
            return '-'.join([password[i:i+4] for i in range(0, len(password), 4)])
        return password

    @staticmethod
    def normalize_length(password):
        """
        填充密码长度
        :param password: str, 16位Hash值
        :return:
        """
        min_len, max_len = 16, 20
        if len(password) < min_len:
            return (password * 2)[:max_len]
        return password[:max_len]

    def generate_password(self):
        if not self.validate_inputs():
            return

        try:
            base = self.base_pw.text()
            final_password = self.apply_rules(base)
            self.result.setText(final_password)
            self.result.setStyleSheet("")
        except Exception as e:
            logger.error(f"生成错误: {str(e)}")
            self.show_error(f"生成错误: {str(e)}")

    def show_error(self, message):
        self.result.setStyleSheet("color: red; background-color: #ffe0e0;")
        self.result.setText(message)

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.result.text())
        self.result.setStyleSheet("background-color: #e0ffe0;")
        QApplication.processEvents()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = PersonPasswordGeneratorApp()
    window.show()
    sys.exit(app.exec_())