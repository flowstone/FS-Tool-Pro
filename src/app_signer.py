import subprocess

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGroupBox, QHBoxLayout, QLineEdit
)
from loguru import logger

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil


class AppSignerApp(QWidget):
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_APP_SIGNER} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_APP_SIGNER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("应用程序签名工具")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        #title_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #333;")
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)


        # 签名应用程序的部分
        sign_app_group = QGroupBox("签名应用程序")
        sign_app_layout = QVBoxLayout()

        # 上传应用程序文件
        app_file_label = QLabel("选择应用程序文件：")
        self.app_file_input = QLineEdit()
        self.upload_app_btn = QPushButton("选择")
        self.upload_app_btn.setObjectName("browse_button")
        self.upload_app_btn.clicked.connect(self.upload_application_file)
        app_layout = QHBoxLayout()
        app_layout.addWidget(self.app_file_input)
        app_layout.addWidget(self.upload_app_btn)
        sign_app_layout.addWidget(app_file_label)
        sign_app_layout.addLayout(app_layout)

        # 上传私钥文件
        key_file_label = QLabel("选择私钥文件：")
        self.key_file_input = QLineEdit()
        self.upload_key_btn = QPushButton("选择")
        self.upload_key_btn.setObjectName("browse_button")
        self.upload_key_btn.clicked.connect(self.upload_key_file)
        key_layout = QHBoxLayout()
        key_layout.addWidget(self.key_file_input)
        key_layout.addWidget(self.upload_key_btn)
        sign_app_layout.addWidget(key_file_label)
        sign_app_layout.addLayout(key_layout)

        # 签名按钮
        self.sign_app_btn = QPushButton("签名应用")
        self.sign_app_btn.clicked.connect(self.sign_application)
        sign_app_layout.addWidget(self.sign_app_btn)

        sign_app_group.setLayout(sign_app_layout)
        layout.addWidget(sign_app_group)

        # 验证签名的部分
        verify_sign_group = QGroupBox("验证签名")
        verify_sign_layout = QVBoxLayout()

        # 上传验证的应用程序文件
        verify_app_file_label = QLabel("选择验证的应用程序文件：")
        self.verify_app_file_input = QLineEdit()
        self.upload_verify_app_btn = QPushButton("选择")
        self.upload_verify_app_btn.setObjectName("browse_button")
        self.upload_verify_app_btn.clicked.connect(self.upload_verify_application_file)
        verify_app_layout = QHBoxLayout()
        verify_app_layout.addWidget(self.verify_app_file_input)
        verify_app_layout.addWidget(self.upload_verify_app_btn)
        verify_sign_layout.addWidget(verify_app_file_label)
        verify_sign_layout.addLayout(verify_app_layout)

        # 上传签名文件
        signature_file_label = QLabel("选择签名文件：")
        self.signature_file_input = QLineEdit()
        self.upload_signature_btn = QPushButton("选择")
        self.upload_signature_btn.setObjectName("browse_button")
        self.upload_signature_btn.clicked.connect(self.upload_signature_file)
        signature_layout = QHBoxLayout()
        signature_layout.addWidget(self.signature_file_input)
        signature_layout.addWidget(self.upload_signature_btn)
        verify_sign_layout.addWidget(signature_file_label)
        verify_sign_layout.addLayout(signature_layout)

        # 上传证书文件
        cert_file_label = QLabel("选择公钥文件：")
        self.cert_file_input = QLineEdit()
        self.upload_cert_btn = QPushButton("选择")
        self.upload_cert_btn.setObjectName("browse_button")
        self.upload_cert_btn.clicked.connect(self.upload_cert_file)
        cert_layout = QHBoxLayout()
        cert_layout.addWidget(self.cert_file_input)
        cert_layout.addWidget(self.upload_cert_btn)
        verify_sign_layout.addWidget(cert_file_label)
        verify_sign_layout.addLayout(cert_layout)

        # 验证签名按钮
        self.verify_signature_btn = QPushButton("验证签名")
        self.verify_signature_btn.clicked.connect(self.verify_signature)
        verify_sign_layout.addWidget(self.verify_signature_btn)

        verify_sign_group.setLayout(verify_sign_layout)
        layout.addWidget(verify_sign_group)

        self.setLayout(layout)


    def upload_application_file(self):
        """上传应用程序文件"""
        self.app_file, _ = QFileDialog.getOpenFileName(self, "选择应用程序文件")
        self.app_file_input.setText(self.app_file)

    def upload_key_file(self):
        """上传私钥文件"""
        self.key_file, _ = QFileDialog.getOpenFileName(self, "选择私钥文件", "", "Key 文件 (*.pem)")
        self.key_file_input.setText(self.key_file)

    def sign_application(self):
        """签名应用程序"""
        if not hasattr(self, "app_file") or not self.app_file:
            MessageUtil.show_warning_message("请先选择应用程序文件！")
            return
        if not hasattr(self, "key_file") or not self.key_file:
            MessageUtil.show_warning_message("请先选择私钥文件！")
            return
        signature_file = self.app_file + ".sig"

        try:
            subprocess.run(
                ["openssl", "dgst", "-sha256", "-sign", self.key_file, "-out", signature_file, self.app_file],
                check=True
            )
            MessageUtil.show_success_message(f"应用程序签名成功！\n签名文件: {signature_file}")
        except subprocess.CalledProcessError as e:
            logger.error(f"签名失败：\n{e}")
            MessageUtil.show_error_message(f"签名失败：\n{e}")
        except Exception as e:
            logger.error(f"签名失败：\n{e}")
            MessageUtil.show_error_message(f"签名失败：\n{e}")

    def upload_verify_application_file(self):
        """上传验证的应用程序文件"""
        self.verify_app_file, _ = QFileDialog.getOpenFileName(self, "选择验证的应用程序文件")
        self.verify_app_file_input.setText(self.verify_app_file)

    def upload_signature_file(self):
        """上传签名文件"""
        self.signature_file, _ = QFileDialog.getOpenFileName(self, "选择签名文件", "", "签名文件 (*.sig)")
        self.signature_file_input.setText(self.signature_file)

    def upload_cert_file(self):
        """上传证书文件"""
        self.cert_file, _ = QFileDialog.getOpenFileName(self, "选择证书文件", "", "PEM 文件 (*.pem)")
        self.cert_file_input.setText(self.cert_file)

    def verify_signature(self):
        """验证签名"""
        if not hasattr(self, "verify_app_file") or not self.verify_app_file:
            MessageUtil.show_warning_message("请先选择验证的应用程序文件！")
            return
        if not hasattr(self, "signature_file") or not self.signature_file:
            MessageUtil.show_warning_message("请先选择签名文件！")
            return
        if not hasattr(self, "cert_file") or not self.cert_file:
            MessageUtil.show_warning_message("请先选择证书文件！")
            return
        try:
            result = subprocess.run(
                ["openssl", "dgst", "-sha256", "-verify", self.cert_file, "-signature", self.signature_file, self.verify_app_file],
                check=True,
                capture_output=True,
                text=True
            )
            if "Verified OK" in result.stdout:
                MessageUtil.show_success_message(f"签名验证成功！\n{result.stdout}")
            else:
                MessageUtil.show_error_message(f"签名验证失败：\n{result.stdout}")
                logger.error(f"签名验证失败：\n{result.stdout}")
        except subprocess.CalledProcessError as e:
            logger.error(f"签名验证失败：\n{e}")
            MessageUtil.show_error_message(f"签名验证失败：\n{e}")
        except Exception as e:
            logger.error(f"签名验证失败：\n{e}")
            MessageUtil.show_error_message(f"签名验证失败：\n{e}")

    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])
    window = AppSignerApp()
    window.show()
    app.exec()
