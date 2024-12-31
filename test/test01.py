import sys
import os
import zipfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QLineEdit, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QClipboard
from PyQt5.QtCore import Qt
from Crypto.PublicKey import RSA


class RSAKeyGeneratorApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("RSA 密钥生成器")
        self.setGeometry(100, 100, 600, 500)

        # 初始化界面组件
        self.init_ui()

        # 初始化密钥内容
        self.public_key = None
        self.private_key = None

    def init_ui(self):
        # 第一行：密钥长度选择和加密方式选择
        self.key_length_label = QLabel("密钥长度:")
        self.key_length_combo = QComboBox()
        self.key_length_combo.addItems(["2048", "3072", "4096"])

        self.encryption_label = QLabel("加密方式:")
        self.encryption_combo = QComboBox()
        self.encryption_combo.addItems(["PKCS#1", "PKCS#8", "OpenSSH"])

        key_settings_layout = QHBoxLayout()
        key_settings_layout.addWidget(self.key_length_label)
        key_settings_layout.addWidget(self.key_length_combo)
        key_settings_layout.addWidget(self.encryption_label)
        key_settings_layout.addWidget(self.encryption_combo)

        # 第二行：操作按钮
        self.generate_button = QPushButton("生成密钥对")
        self.copy_public_button = QPushButton("复制公钥")
        self.copy_private_button = QPushButton("复制私钥")
        self.download_button = QPushButton("下载全部")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.generate_button)
        button_layout.addWidget(self.copy_public_button)
        button_layout.addWidget(self.copy_private_button)
        button_layout.addWidget(self.download_button)

        # 第三行：公钥显示框
        self.public_key_label = QLabel("公钥:")
        self.public_key_text = QTextEdit()
        self.public_key_text.setReadOnly(True)

        # 第四行：私钥显示框
        self.private_key_label = QLabel("私钥:")
        self.private_key_text = QTextEdit()
        self.private_key_text.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        layout.addLayout(key_settings_layout)
        layout.addLayout(button_layout)
        layout.addWidget(self.public_key_label)
        layout.addWidget(self.public_key_text)
        layout.addWidget(self.private_key_label)
        layout.addWidget(self.private_key_text)

        self.setLayout(layout)

        # 信号连接
        self.generate_button.clicked.connect(self.generate_keys)
        self.copy_public_button.clicked.connect(self.copy_public_key)
        self.copy_private_button.clicked.connect(self.copy_private_key)
        self.download_button.clicked.connect(self.download_keys)

    def generate_keys(self):
        """生成 RSA 密钥对"""
        key_length = int(self.key_length_combo.currentText())
        encryption_method = self.encryption_combo.currentText()

        # 生成 RSA 密钥
        key = RSA.generate(key_length)

        # 根据加密方式导出密钥
        if encryption_method == "OpenSSH":
            self.public_key = key.publickey().export_key(format="OpenSSH").decode()
            self.private_key = key.export_key(format="PEM").decode()
        else:
            self.public_key = key.publickey().export_key(
                format="PEM",
                pkcs=1 if encryption_method == "PKCS#1" else 8
            ).decode()
            self.private_key = key.export_key(
                format="PEM",
                pkcs=1 if encryption_method == "PKCS#1" else 8
            ).decode()

        # 显示公钥和私钥
        self.public_key_text.setPlainText(self.public_key)
        self.private_key_text.setPlainText(self.private_key)

    def copy_public_key(self):
        """复制公钥到剪贴板"""
        if self.public_key:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.public_key)
        else:
            self.public_key_text.setPlainText("请先生成密钥对")

    def copy_private_key(self):
        """复制私钥到剪贴板"""
        if self.private_key:
            clipboard = QApplication.clipboard()
            clipboard.setText(self.private_key)
        else:
            self.private_key_text.setPlainText("请先生成密钥对")

    def download_keys(self):
        """将公钥和私钥打包成 ZIP 文件并下载"""
        if not self.public_key or not self.private_key:
            self.private_key_text.setPlainText("请先生成密钥对")
            return

        # 保存文件对话框
        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "保存密钥", "", "ZIP 文件 (*.zip)")

        if save_path:
            if not save_path.endswith(".zip"):
                save_path += ".zip"

            # 创建 ZIP 文件
            with zipfile.ZipFile(save_path, 'w') as zipf:
                zipf.writestr("public_key.txt", self.public_key)
                zipf.writestr("private_key.pem", self.private_key)

            self.private_key_text.setPlainText(f"密钥已保存到: {save_path}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAKeyGeneratorApp()
    window.show()
    sys.exit(app.exec_())
