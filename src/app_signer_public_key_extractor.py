import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.x509 import load_pem_x509_certificate, load_der_x509_certificate

from src.const.fs_constants import FsConstants


class PublicKeyExtractorApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(FsConstants.PUBLIC_KEY_EXTRACTOR_WINDOW_TITLE)
        #self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()

        # 替换 QLabel 为 QLineEdit
        self.cert_path_input = QLineEdit()
        self.cert_path_input.setPlaceholderText("选择证书文件路径...")
        layout.addWidget(self.cert_path_input)

        self.select_button = QPushButton('选择')
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
            "证书文件 (*.pem *.crt *.cer *.der)"
        )
        if file_path:
            # 将文件路径显示在输入框中
            self.cert_path_input.setText(file_path)

    def extract_public_key(self):
        cert_path = self.cert_path_input.text()
        if not cert_path or cert_path.strip() == "":
            self.result_label.setText("请选择或输入一个证书文件路径。")
            return

        try:
            with open(cert_path, 'rb') as cert_file:
                cert_data = cert_file.read()

                # 尝试加载 PEM 或 DER 格式证书
                if b"BEGIN CERTIFICATE" in cert_data:
                    cert = load_pem_x509_certificate(cert_data, default_backend())
                else:
                    cert = load_der_x509_certificate(cert_data, default_backend())

            public_key = cert.public_key()
            public_key_pem = public_key.public_bytes(
                encoding=Encoding.PEM,
                format=PublicFormat.SubjectPublicKeyInfo
            )

            # 保存公钥
            save_path, _ = QFileDialog.getSaveFileName(
                self, "保存公钥文件", "extracted_public_key.pem", "PEM 文件 (*.pem)"
            )
            if save_path:
                with open(save_path, 'wb') as key_file:
                    key_file.write(public_key_pem)
                self.result_label.setText(f"公钥已提取并保存到：{save_path}")
            else:
                self.result_label.setText("保存操作已取消。")

        except Exception as e:
            self.result_label.setText(f"提取公钥时出错: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = PublicKeyExtractor()
    ex.show()
    sys.exit(app.exec_())
