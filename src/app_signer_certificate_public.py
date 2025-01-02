import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog
from cryptography import x509
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.hazmat.backends import default_backend
import os

from cryptography.x509 import load_pem_x509_certificate


class PublicKeyExtractor(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('公钥提取器')
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # 移除 QLineEdit 组件，使用 QLabel 显示文件路径
        self.cert_path_label = QLabel("未选择证书文件。")
        layout.addWidget(self.cert_path_label)

        self.select_button = QPushButton('选择证书文件')
        self.select_button.clicked.connect(self.select_certificate)
        layout.addWidget(self.select_button)

        self.extract_button = QPushButton('提取公钥')
        self.extract_button.clicked.connect(self.extract_public_key)
        layout.addWidget(self.extract_button)

        self.result_label = QLabel()
        layout.addWidget(self.result_label)

        self.setLayout(layout)

    def select_certificate(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "选择证书文件",
            "",
            "证书文件 (*.pem *.crt *.cer)"
        )
        if file_path:
            self.cert_path_label.setText(file_path)

    def extract_public_key(self):
        cert_path = self.cert_path_label.text()
        if not cert_path or cert_path == "未选择证书文件。":
            self.result_label.setText("请选择一个证书文件。")
            return
        try:
            with open(cert_path, 'rb') as cert_file:
                cert = load_pem_x509_certificate(cert_file.read(), default_backend())
            public_key = cert.public_key()
            public_key_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )
            public_key_path = "extracted_public_key.pem"
            with open(public_key_path, 'wb') as key_file:
                key_file.write(public_key_pem)
            self.result_label.setText(f"公钥已提取并保存到 {public_key_path}。")
        except Exception as e:
            self.result_label.setText(f"提取公钥时出错: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PublicKeyExtractor()
    ex.show()
    sys.exit(app.exec_())