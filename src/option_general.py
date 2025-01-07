from PySide6.QtWidgets import (
    QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog, QMessageBox
)
from PySide6.QtGui import QIcon
import os
import sys
import subprocess

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil


class OptionGeneral(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("首选项")
        self.setFixedSize(600, 150)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        # 创建主布局
        main_layout = QVBoxLayout()

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

        # 添加 GroupBox 到主布局
        main_layout.addWidget(group_box)
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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OptionGeneral()
    window.show()
    sys.exit(app.exec())
