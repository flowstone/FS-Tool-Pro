import sys
import zipfile
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QComboBox, QPushButton, QVBoxLayout, QHBoxLayout, QTextEdit, QFileDialog
)
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from Crypto.PublicKey import RSA

from src.const.color_constants import BLACK
from src.util.common_util import CommonUtil
from src.const.font_constants import FontConstants
from loguru import logger


class RSAKeyGeneratorThread(QThread):
    result_signal = pyqtSignal(str, str)  # 用于将公钥和私钥传递回主线程
    error_signal = pyqtSignal(str)  # 用于传递错误消息

    def __init__(self, key_length, encryption_method):
        super().__init__()
        self.key_length = key_length
        self.encryption_method = encryption_method

    def run(self):
        try:
            # 生成 RSA 密钥对
            key = RSA.generate(self.key_length)
            if self.encryption_method == "OpenSSH":
                public_key = key.publickey().export_key(format="OpenSSH").decode()
                private_key = key.export_key(format="PEM").decode()
            else:
                public_key = key.publickey().export_key(
                    format="PEM",
                    pkcs=1 if self.encryption_method == "PKCS#1" else 8
                ).decode()
                private_key = key.export_key(
                    format="PEM",
                    pkcs=1 if self.encryption_method == "PKCS#1" else 8
                ).decode()

            # 发出结果信号
            self.result_signal.emit(public_key, private_key)

        except Exception as e:
            self.error_signal.emit(str(e))


class RSAKeyGeneratorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setWindowTitle("RSA密钥生成器")
        self.setFixedSize(700, 600)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 初始化界面组件
        self.init_ui()

        # 初始化密钥内容
        self.public_key = None
        self.private_key = None

        # 初始化线程对象
        self.thread = None

    def init_ui(self):
        # 第一行：密钥长度选择和加密方式选择
        key_length_label = QLabel("密钥长度:")
        self.key_length_combo = QComboBox()
        self.key_length_combo.addItems(["2048", "3072", "4096"])

        encryption_label = QLabel("加密方式:")
        self.encryption_combo = QComboBox()
        self.encryption_combo.addItems(["PKCS#1", "PKCS#8", "OpenSSH"])

        key_settings_layout = QHBoxLayout()
        key_settings_layout.addWidget(key_length_label)
        key_settings_layout.addWidget(self.key_length_combo)
        key_settings_layout.addWidget(encryption_label)
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
        public_key_label = QLabel("公钥:")
        self.public_key_text = QTextEdit()
        self.public_key_text.setReadOnly(True)

        # 第四行：私钥显示框
        private_key_label = QLabel("私钥:")
        self.private_key_text = QTextEdit()
        self.private_key_text.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        title_label = QLabel("RSA密钥生成器")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)

        layout.addLayout(key_settings_layout)
        layout.addLayout(button_layout)
        layout.addWidget(public_key_label)
        layout.addWidget(self.public_key_text)
        layout.addWidget(private_key_label)
        layout.addWidget(self.private_key_text)

        self.setLayout(layout)

        # 信号连接
        self.generate_button.clicked.connect(self.start_key_generation)
        self.copy_public_button.clicked.connect(self.copy_public_key)
        self.copy_private_button.clicked.connect(self.copy_private_key)
        self.download_button.clicked.connect(self.download_keys)

    def start_key_generation(self):
        """启动密钥生成线程"""
        key_length = int(self.key_length_combo.currentText())
        encryption_method = self.encryption_combo.currentText()

        # 禁用按钮，防止重复操作
        self.generate_button.setEnabled(False)
        self.public_key_text.setPlainText("正在生成公钥，请稍候……")
        self.private_key_text.setPlainText("正在生成私钥，请稍候……")

        # 启动线程
        self.thread = RSAKeyGeneratorThread(key_length, encryption_method)
        self.thread.result_signal.connect(self.on_key_generated)
        self.thread.error_signal.connect(self.on_error)
        self.thread.start()

    def on_key_generated(self, public_key, private_key):
        """接收线程生成的密钥并更新 UI"""
        self.public_key = public_key
        self.private_key = private_key

        self.public_key_text.setPlainText(self.public_key)
        self.private_key_text.setPlainText(self.private_key)

        # 恢复按钮可用状态
        self.generate_button.setEnabled(True)

    def on_error(self, error_message):
        """处理线程中的错误"""
        self.public_key_text.setPlainText(f"生成公钥失败：{error_message}")
        self.private_key_text.setPlainText(f"生成私钥失败：{error_message}")

        # 恢复按钮可用状态
        self.generate_button.setEnabled(True)

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

        file_dialog = QFileDialog()
        save_path, _ = file_dialog.getSaveFileName(self, "保存密钥", "", "ZIP 文件 (*.zip)")

        if save_path:
            if not save_path.endswith(".zip"):
                save_path += ".zip"

            with zipfile.ZipFile(save_path, 'w') as zipf:
                zipf.writestr("public_key.pem", self.public_key)
                zipf.writestr("private_key.pem", self.private_key)

            self.private_key_text.setPlainText(f"密钥已保存到: {save_path}")

    def closeEvent(self, event):
        logger.info("点击了关闭事件")
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RSAKeyGeneratorApp()
    window.show()
    sys.exit(app.exec_())
