import os
import shutil
import sys

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from loguru import logger

from src.const.color_constants import BLUE, BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar


class CreateFolderApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  Signal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_CREATE_FOLDER} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_CREATE_FOLDER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setFixedHeight(300)
        # 设置窗口背景色为淡灰色
        self.setAutoFillBackground(True)
        self.setAcceptDrops(True)



        layout = QVBoxLayout()
        title_label = QLabel("批量生成文件夹")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)
        # 说明文本
        description_label = QLabel("根据输入的分割字符，取前部分创建文件夹，符合相关的文件都移动到对应文件夹中")
        description_label.setFont(FontConstants.ITALIC_SMALL)

        # 选择文件夹相关部件
        folder_path_label = QLabel("选择文件夹：")
        folder_path_layout = QHBoxLayout()
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setObjectName("folder_path_input")
        browse_button = QPushButton("选择")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(self.folder_path_entry)
        folder_path_layout.addWidget(browse_button)

        # 指定分割字符相关部件
        slice_label = QLabel("指定分割字符：")
        self.slice_entry = QLineEdit()



        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.clicked.connect(self.start_operation)

        exit_button = QPushButton("退出")
        exit_button.clicked.connect(self.close)

        button_layout.addWidget(start_button)
        button_layout.addWidget(exit_button)

        # 布局调整
        layout.addWidget(description_label)
        layout.addWidget(folder_path_label)
        layout.addLayout(folder_path_layout)
        layout.addWidget(slice_label)
        layout.addWidget(self.slice_entry)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        layout.addLayout(button_layout)

        self.setLayout(layout)




    def browse_folder(self):
        logger.info("---- 开始选择文件夹 ----")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_entry.setText(folder_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            folder_path = event.mimeData().urls()[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.folder_path_entry.setText(folder_path)
            else:
                MessageUtil.show_warning_message("拖入的不是有效文件夹！")

    def start_operation(self):
        logger.info("---- 开始执行操作 ----")

        folder_path = self.folder_path_entry.text()
        slice_char = self.slice_entry.text()
        if folder_path:
            self.setEnabled(False)
            self.worker_thread = FileOperationThread(folder_path, slice_char)
            self.worker_thread.finished_signal.connect(self.operation_finished)
            self.worker_thread.progress_signal.connect(self.progress_bar.update_progress)
            self.worker_thread.error_signal.connect(self.operation_error)
            self.worker_thread.start()
            self.progress_bar.show()
        else:
            MessageUtil.show_warning_message("请选择要操作的文件夹！")

    def operation_finished(self):
        logger.info("---- 操作完成 ----")
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_success_message("移动文件完成！")

    def operation_error(self, error_msg):
        logger.error(f"出现异常：{error_msg}")
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_warning_message("遇到异常停止工作")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

class FileOperationThread(QThread):
    progress_signal = Signal(int)
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, folder_path, slice_char):
        super().__init__()
        self.folder_path = folder_path
        self.slice_char = slice_char


    def run(self):
        try:

            if self.slice_char != "":
                logger.info("---- 有分割字符，开始执行操作 ----")
                files = os.listdir(self.folder_path)
                total_files = len([f for f in files if os.path.isfile(os.path.join(self.folder_path, f))])

                self.create_folder_move_files(self.folder_path, self.slice_char, total_files)
            else:
                logger.info("---- 分割字符为空，不执行操作 ----")
            self.finished_signal.emit()

        except OSError as e:
            self.error_signal.emit(str(e))

    def create_folder_move_files(self, folder_path, slice_char, total_files):
        # 遍历文件夹下的文件名
        processed_files = 0

        for filename in os.listdir(folder_path):
            source_path = os.path.join(folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(source_path):
                # 找到分割的位置，如'-'
                index = filename.find(slice_char)
                if index != -1:
                    # 提取 '-' 前面的部分作为文件夹名
                    folder_name = filename[:index]
                    # 如果文件夹不存在，则创建
                    target_folder = os.path.join(folder_path, folder_name)
                    if not os.path.exists(target_folder):
                        os.mkdir(target_folder)
                    # 将文件移动到对应的文件夹
                    destination_path = os.path.join(target_folder, filename)
                    shutil.move(source_path, destination_path)
                    # 更新进度条
                    processed_files += 1
                    self.progress_signal.emit(processed_files)  # 发出进度信号

                # 处理完成后退出循环
                if processed_files == total_files:
                    break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CreateFolderApp()
    window.show()
    sys.exit(app.exec())