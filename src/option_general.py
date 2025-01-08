from PySide6.QtWidgets import (
    QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox, QCheckBox
)
from PySide6.QtGui import QIcon
import os
import sys
import subprocess

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.load_config import get_ini_flask_flag, set_ini_flask_flag
from src.util.message_util import MessageUtil


class OptionGeneral(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("首选项")
        self.setFixedWidth(600)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 创建主布局
        main_layout = QVBoxLayout()
        base_group_box = QGroupBox("基础配置")
        base_group_box_layout = QVBoxLayout()
        self.flask_checkbox = QCheckBox("Flask服务")
        # 从配置文件加载 Flask 服务是否启用的配置
        if get_ini_flask_flag():
            self.flask_checkbox.setChecked(True)
        base_group_box_layout.addWidget(self.flask_checkbox)
        base_group_box.setLayout(base_group_box_layout)
        main_layout.addWidget(base_group_box)

        # 创建 GroupBox
        group_box = QGroupBox("配置文件存储位置")
        group_box_layout = QVBoxLayout()

        # 第一行：标签和输入框
        input_layout = QHBoxLayout()
        path_label = QLabel("路径:")
        self.path_input = QLineEdit()
        app_ini_file = os.path.join(CommonUtil.get_external_path(), FsConstants.EXTERNAL_APP_INI_FILE)
        self.path_input.setText(app_ini_file)
        self.path_input.setReadOnly(True)
        input_layout.addWidget(path_label)
        input_layout.addWidget(self.path_input)

        # 第二行：按钮
        button_layout = QHBoxLayout()
        open_dir_button = QPushButton("打开文件所在目录")
        open_file_button = QPushButton("打开文件")
        button_layout.addWidget(open_dir_button)
        button_layout.addWidget(open_file_button)

        # 绑定按钮事件
        open_dir_button.clicked.connect(self.open_directory)
        open_file_button.clicked.connect(self.open_file)

        # 将布局添加到 GroupBox
        group_box_layout.addLayout(input_layout)
        group_box_layout.addLayout(button_layout)
        group_box.setLayout(group_box_layout)

        main_layout.addWidget(group_box)
        # 保存按钮 - 右对齐
        save_button_layout = QHBoxLayout()
        save_button_layout.addStretch()  # 添加一个弹性空间
        save_button = QPushButton("保存")
        save_button.clicked.connect(self.save_settings)
        save_button_layout.addWidget(save_button)
        main_layout.addLayout(save_button_layout)
        self.setLayout(main_layout)

    def open_directory(self):
        """打开文件所在目录"""
        file_path = self.path_input.text().strip()
        if not file_path or not os.path.exists(file_path):
            QMessageBox.warning(self, "错误", "请输入有效的文件路径！")
            return

        # 获取目录路径
        dir_path = os.path.dirname(file_path)
        try:
            if CommonUtil.check_win_os():
                subprocess.Popen(f'explorer "{dir_path}"')
            elif CommonUtil.check_mac_os():
                subprocess.Popen(["open", dir_path])
            else:
                subprocess.Popen(["xdg-open", dir_path])
        except Exception as e:
            MessageUtil.show_error_message(f"无法打开目录: {e}")

    def open_file(self):
        """打开文件"""
        file_path = self.path_input.text().strip()
        if not file_path or not os.path.isfile(file_path):
            MessageUtil.show_warning_message("请输入有效的文件路径！")
            return

        try:
            if CommonUtil.check_win_os():
                os.startfile(file_path)
            elif CommonUtil.check_mac_os():
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
        except Exception as e:
            MessageUtil.show_error_message(f"无法打开目录: {e}")

    def save_settings(self):
        """保存设置到 ini 文件"""
        flask_enabled = self.flask_checkbox.isChecked()
        try:
            set_ini_flask_flag(flask_enabled)  # 将 Flask 服务的状态写入到配置文件
            MessageUtil.show_success_message("设置已成功保存！")
        except Exception as e:
            MessageUtil.show_error_message(f"保存设置失败: {e}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptionGeneral()
    window.show()
    sys.exit(app.exec())
