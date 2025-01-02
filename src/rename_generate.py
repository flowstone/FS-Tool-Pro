import os
import sys
import time
import uuid

from PyQt5.QtCore import QThread
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QGroupBox, QRadioButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog
)
from loguru import logger

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar


class RenameGenerateApp(QWidget):
    closed_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.check_type_text = None
        self.naming_type = "序号"
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_RENAME_GENERATE} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_RENAME_GENERATE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("批量修改文件/文件夹名")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)
        # 文件夹选择
        folder_label = QLabel("选择文件夹：")
        layout.addWidget(folder_label)
        folder_layout = QHBoxLayout()
        self.folder_entry = QLineEdit()
        self.folder_entry.setObjectName("folder_path_input")
        self.browse_button = QPushButton("选择")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_entry)
        folder_layout.addWidget(self.browse_button)
        layout.addLayout(folder_layout)

        # 文件类型选择
        file_group_layout = QVBoxLayout()
        file_group = QGroupBox("文件类型")
        radio_btn_layout = QHBoxLayout()
        self.file_rbtn = QRadioButton("文件")
        self.folder_rbtn = QRadioButton("文件夹")
        self.file_rbtn.setChecked(True)  # 默认选中选项1
        self.check_type_text = self.file_rbtn.text()
        self.file_rbtn.toggled.connect(self.radio_btn_toggled)
        self.folder_rbtn.toggled.connect(self.radio_btn_toggled)
        radio_btn_layout.addWidget(self.file_rbtn)
        radio_btn_layout.addWidget(self.folder_rbtn)
        file_group.setLayout(radio_btn_layout)
        file_group_layout.addWidget(file_group)
        layout.addLayout(file_group_layout)



        # 命名规则选择
        naming_group_layout = QVBoxLayout()
        naming_group = QGroupBox("命名规则")
        naming_layout = QVBoxLayout()
        self.naming_rbtns = {
            "序号": QRadioButton("序号 (1, 2, 3)"),
            "UUID": QRadioButton("UUID"),
            "时间+序号": QRadioButton("时间+序号"),
            "时间+UUID": QRadioButton("时间+UUID"),
        }
        self.naming_rbtns["序号"].setChecked(True)
        for key, btn in self.naming_rbtns.items():
            btn.toggled.connect(self.naming_toggled)
            naming_layout.addWidget(btn)
        naming_group.setLayout(naming_layout)
        naming_group_layout.addWidget(naming_group)
        layout.addLayout(naming_group_layout)

        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_operation)

        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def radio_btn_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.check_type_text = radio_button.text()
            logger.info(f"选择类型：{radio_button.text()}")

    def naming_toggled(self):
        for key, btn in self.naming_rbtns.items():
            if btn.isChecked():
                self.naming_type = key
                logger.info(f"选择命名规则：{key}")

    def browse_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_entry.setText(folder_path)

    def start_operation(self):

        folder_path = self.folder_entry.text()
        if folder_path:
            self.setEnabled(False)
            self.progress_bar.set_range(0,0)

            self.worker_thread = FileRenameThread(folder_path, self.check_type_text, self.naming_type)
            self.worker_thread.finished_signal.connect(self.operation_finished)
            self.worker_thread.error_signal.connect(self.operation_error)
            self.worker_thread.start()
            self.progress_bar.show()

        else:
            MessageUtil.show_warning_message("请选择一个文件夹！")
            logger.warning("未选择文件夹")

    def operation_finished(self):
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_success_message("重命名完成！")
        logger.info("---- 重命名操作完成 ----")

    def operation_error(self, error_msg):
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_error_message(f"遇到错误：{error_msg}")
        logger.error(f"错误：{error_msg}")

    def closeEvent(self, event):
        self.closed_signal.emit()
        super().closeEvent(event)



class FileRenameThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, folder_path, check_type, naming_type):
        super().__init__()
        self.folder_path = folder_path
        self.check_type = check_type
        self.naming_type = naming_type

    def run(self):
        try:
            if self.check_type == "文件":
                logger.info(f"你选择类型是:{FsConstants.FILE_RENAMER_TYPE_FILE}")
                self.rename_files()
            else:
                logger.info(f"你选择的类型是：{FsConstants.FILE_RENAMER_TYPE_FOLDER}")
                self.rename_folders()
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

    def rename_files(self):
        for idx, filename in enumerate(os.listdir(self.folder_path), start=1):
            old_path = os.path.join(self.folder_path, filename)
            if os.path.isfile(old_path):
                new_filename = self.generate_name(idx) + os.path.splitext(filename)[1]
                new_path = os.path.join(self.folder_path, new_filename)
                os.rename(old_path, new_path)

    def rename_folders(self):
        for idx, folder_name in enumerate(os.listdir(self.folder_path), start=1):
            old_path = os.path.join(self.folder_path, folder_name)
            if os.path.isdir(old_path):
                new_folder_name = self.generate_name(idx)
                new_path = os.path.join(self.folder_path, new_folder_name)
                os.rename(old_path, new_path)

    def generate_name(self, idx):
        if self.naming_type == "序号":
            return f"{idx}"
        elif self.naming_type == "UUID":
            return str(uuid.uuid4())
        elif self.naming_type == "时间+序号":
            return time.strftime("%Y%m%d_%H%M%S") + "_" + f"{idx}"
        elif self.naming_type == "时间+UUID":
            return time.strftime("%Y%m%d_%H%M%S") + "_" + str(uuid.uuid4())
        return "unknown"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameBaseApp()
    window.show()
    sys.exit(app.exec_())