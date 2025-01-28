import os
import sys
import time
import uuid

from PySide6.QtCore import QThread
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QApplication, QGroupBox, QRadioButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QFileDialog
)
from fs_base.message_util import MessageUtil
from fs_base.widget import TransparentTextBox, CustomProgressBar
from loguru import logger

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil

from src.widget.sub_window_widget import SubWindowWidget


class RenameGenerateApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.check_type_text = None
        self.naming_type = "序号"
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_RENAME_GENERATE} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_RENAME_GENERATE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()

        # 标题
        title_label = QLabel("批量随机文件重命名")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
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



        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.start_button.clicked.connect(self.start_operation)

        button_layout.addWidget(self.start_button)
        layout.addLayout(button_layout)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        layout.addWidget(TransparentTextBox())
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
            self.worker_thread = FileRenameThread(folder_path, self.check_type_text, self.naming_type)
            self.worker_thread.finished_signal.connect(self.operation_finished)
            self.worker_thread.progress_signal.connect(self.progress_bar.update_progress)  # 连接进度信号

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
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            folder_path = event.mimeData().urls()[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.folder_entry.setText(folder_path)
            else:
                MessageUtil.show_warning_message("拖入的不是有效文件夹！")



class FileRenameThread(QThread):
    finished_signal = Signal()
    error_signal = Signal(str)
    progress_signal = Signal(int)  # 新增信号，发送当前进度百分比

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
        files = [f for f in os.listdir(self.folder_path) if os.path.isfile(os.path.join(self.folder_path, f))]
        total_files = len(files)
        for idx, filename in enumerate(files, start=1):
            old_path = os.path.join(self.folder_path, filename)
            new_filename = self.generate_name(idx) + os.path.splitext(filename)[1]
            new_path = os.path.join(self.folder_path, new_filename)
            os.rename(old_path, new_path)

            # 发送进度信号
            progress = int((idx / total_files) * 100)
            self.progress_signal.emit(progress)

    def rename_folders(self):
        folders = [f for f in os.listdir(self.folder_path) if os.path.isdir(os.path.join(self.folder_path, f))]
        total_folders = len(folders)
        for idx, folder_name in enumerate(folders, start=1):
            old_path = os.path.join(self.folder_path, folder_name)
            new_folder_name = self.generate_name(idx)
            new_path = os.path.join(self.folder_path, new_folder_name)
            os.rename(old_path, new_path)

            # 发送进度信号
            progress = int((idx / total_folders) * 100)
            self.progress_signal.emit(progress)

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
    window = RenameGenerateApp()
    window.show()
    sys.exit(app.exec())
