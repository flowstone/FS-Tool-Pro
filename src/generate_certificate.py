import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTextEdit, QFileDialog, QMessageBox
)
from PyQt5.QtCore import Qt
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography import x509
from cryptography.x509.oid import NameOID
from datetime import datetime, timedelta


class GenerateCertificateApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("应用程序自签名工具")
        self.setGeometry(100, 100, 600, 500)

        # 界面组件
        self.label_common_name = QLabel("Common Name (CN):")
        self.input_common_name = QLineEdit()
        self.label_organization = QLabel("Organization (O):")
        self.input_organization = QLineEdit()
        self.label_country = QLabel("Country Code (C):")
        self.input_country = QLineEdit()
        self.button_generate = QPushButton("生成自签名证书")
        self.button_save = QPushButton("保存证书和私钥")
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label_common_name)
        layout.addWidget(self.input_common_name)
        layout.addWidget(self.label_organization)
        layout.addWidget(self.input_organization)
        layout.addWidget(self.label_country)
        layout.addWidget(self.input_country)
        layout.addWidget(self.button_generate)
        layout.addWidget(self.button_save)
        layout.addWidget(self.text_output)
        self.setLayout(layout)

        # 连接按钮事件
        self.button_generate.clicked.connect(self.generate_certificate)
        self.button_save.clicked.connect(self.save_files)

        # 存储证书和私钥
        self.private_key = None
        self.certificate = None

    def generate_certificate(self):
        """
        生成自签名证书
        """
        common_name = self.input_common_name.text().strip()
        organization = self.input_organization.text().strip()
        country = self.input_country.text().strip()

        if not common_name or not organization or not country:
            QMessageBox.warning(self, "输入错误", "请填写所有字段。")
            return

        if len(country) != 2:
            QMessageBox.warning(self, "输入错误", "国家代码必须是2个字母（如：CN）。")
            return

        try:
            # 生成 RSA 私钥
            self.private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
            )

            # 创建证书主题
            subject = x509.Name([
                x509.NameAttribute(NameOID.COUNTRY_NAME, country),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, organization),
                x509.NameAttribute(NameOID.COMMON_NAME, common_name),
            ])

            # 创建自签名证书
            self.certificate = x509.CertificateBuilder().subject_name(
                subject
            ).issuer_name(
                subject  # 自签名，颁发者和主题相同
            ).public_key(
                self.private_key.public_key()
            ).serial_number(
                x509.random_serial_number()
            ).not_valid_before(
                datetime.utcnow()
            ).not_valid_after(
                datetime.utcnow() + timedelta(days=365)  # 有效期 1 年
            ).sign(self.private_key, hashes.SHA256())

            # 显示证书信息
            cert_pem = self.certificate.public_bytes(serialization.Encoding.PEM).decode("utf-8")
            self.text_output.setText(f"自签名证书生成成功！\n\n{cert_pem}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"生成证书时出错: {str(e)}")

    def save_files(self):
        """
        保存证书和私钥到文件
        """
        if not self.private_key or not self.certificate:
            QMessageBox.warning(self, "提示", "请先生成证书和私钥。")
            return

        save_dir = QFileDialog.getExistingDirectory(self, "选择保存目录")
        if not save_dir:
            return

        try:
            # 保存私钥
            private_key_path = f"{save_dir}/private_key.pem"
            private_key_pem = self.private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption(),
            )
            with open(private_key_path, "wb") as f:
                f.write(private_key_pem)

            # 保存证书
            cert_path = f"{save_dir}/certificate.pem"
            cert_pem = self.certificate.public_bytes(serialization.Encoding.PEM)
            with open(cert_path, "wb") as f:
                f.write(cert_pem)

            QMessageBox.information(self, "成功", f"文件保存成功！\n私钥: {private_key_path}\n证书: {cert_path}")

        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存文件时出错: {str(e)}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SelfSignerApp()
    window.show()
    sys.exit(app.exec_())
