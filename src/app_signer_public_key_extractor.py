import sys

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog, QLineEdit
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat
from cryptography.x509 import load_pem_x509_certificate, load_der_x509_certificate
from fs_base.widget import TransparentTextBox
from loguru import logger

from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class PublicKeyExtractorApp(SubWindowWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_APP_SIGNER_PUBLIC_KEY_EXTRACTOR} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_APP_SIGNER_PUBLIC_KEY_EXTRACTOR)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        layout = QVBoxLayout()
        # 说明文本
        description_label = QLabel("从证书文件中提取公钥，以提供给签名工具使用。")
        description_label.setFont(FontConstants.ITALIC_SMALL)
        layout.addWidget(description_label)
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
        layout.addWidget(TransparentTextBox())
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
    ex = PublicKeyExtractorApp()
    ex.show()
    sys.exit(app.exec())
