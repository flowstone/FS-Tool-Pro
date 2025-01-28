import os
import shutil
import sys

from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from fs_base.widget import CustomProgressBar, TransparentTextBox
from loguru import logger

from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class MoveFileApp(SubWindowWidget):


    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(F"---- 初始化{FsConstants.WINDOW_TITLE_MOVE_FILE} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_MOVE_FILE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        # self.setFixedHeight(300)
        # self.setMinimumHeight(300)
        # 布局设计
        layout = QVBoxLayout()
        title_label = QLabel("批量移动文件")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)
        # 说明文本
        description_label = QLabel("移动指定目录下的所有文件到指定目录")
        description_label.setFont(FontConstants.ITALIC_SMALL)
        layout.addWidget(description_label)
        # 操作目录选择
        src_label = QLabel("选择操作目录：")
        src_layout = QHBoxLayout()
        self.src_entry = QLineEdit()
        browse_src_button = QPushButton("选择")
        browse_src_button.setObjectName("browse_button")
        browse_src_button.clicked.connect(self.browse_src_folder)
        src_layout.addWidget(self.src_entry)
        src_layout.addWidget(browse_src_button)

        # 保存目录选择
        dest_label = QLabel("选择保存目录：")
        dest_layout = QHBoxLayout()
        self.dest_entry = QLineEdit()
        browse_dest_button = QPushButton("选择")
        browse_dest_button.setObjectName("browse_button")
        browse_dest_button.clicked.connect(self.browse_dest_folder)
        dest_layout.addWidget(self.dest_entry)
        dest_layout.addWidget(browse_dest_button)

        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.clicked.connect(self.start_operation)

        button_layout.addWidget(start_button)

        # 布局调整
        layout.addWidget(src_label)
        layout.addLayout(src_layout)
        layout.addWidget(dest_label)
        layout.addLayout(dest_layout)


        layout.addLayout(button_layout)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        layout.addWidget(TransparentTextBox())
        self.setLayout(layout)

    def browse_src_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择操作目录")
        self.src_entry.setText(folder_path)

    def browse_dest_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "选择保存目录")
        self.dest_entry.setText(folder_path)

    def start_operation(self):
        src_folder = self.src_entry.text()
        dest_folder = self.dest_entry.text()

        if not src_folder or not dest_folder:
            logger.warning("请选择操作目录和保存目录！")
            self.show_message("警告", "请选择操作目录和保存目录！")
            return

        if not os.path.exists(src_folder) or not os.path.isdir(src_folder):
            logger.warning("操作目录无效！")
            self.show_message("错误", "操作目录无效！")
            return

        if not os.path.exists(dest_folder) or not os.path.isdir(dest_folder):
            logger.warning("保存目录无效！")
            self.show_message("错误", "保存目录无效！")
            return

        self.setEnabled(False)
        self.worker_thread = FileMoveThread(src_folder, dest_folder)
        self.worker_thread.progress_signal.connect(self.progress_bar.update_progress)
        self.worker_thread.finished_signal.connect(self.operation_finished)
        self.worker_thread.error_signal.connect(self.operation_error)
        self.worker_thread.start()
        self.progress_bar.show()

    def operation_finished(self):
        self.setEnabled(True)
        self.progress_bar.hide()
        self.show_message("成功", "文件移动完成！")

    def operation_error(self, error_msg):
        self.setEnabled(True)
        self.progress_bar.hide()
        self.show_message("错误", f"遇到异常：{error_msg}")

    def show_message(self, title, message):
        from PySide6.QtWidgets import QMessageBox
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.exec()



class FileMoveThread(QThread):
    progress_signal = Signal(int)

    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, src_folder, dest_folder):
        super().__init__()
        self.src_folder = src_folder
        self.dest_folder = dest_folder

    def run(self):
        try:
            logger.info("---- 开始移动文件 ----")
            files_to_move = []
            for root, _, files in os.walk(self.src_folder):
                for file in files:
                    files_to_move.append(os.path.join(root, file))

            total_files = len(files_to_move)
            if total_files == 0:
                self.finished_signal.emit()
                return

            for index, src_path in enumerate(files_to_move):
                file_name = os.path.basename(src_path)
                dest_path = os.path.join(self.dest_folder, file_name)

                # 如果文件已存在，重命名目标文件
                dest_path = self.get_unique_path(dest_path)

                shutil.move(src_path, dest_path)
                logger.info(f"移动文件：{src_path} -> {dest_path}")

                # 更新进度
                progress = int((index + 1) / total_files * 100)
                self.progress_signal.emit(progress)

            self.finished_signal.emit()
        except Exception as e:
            logger.error(f"文件移动时出现异常：{e}")
            self.error_signal.emit(str(e))

    @staticmethod
    def get_unique_path(dest_path):
        """
        如果目标路径已存在，生成一个唯一的文件名。
        """
        base, ext = os.path.splitext(dest_path)
        counter = 1
        while os.path.exists(dest_path):
            dest_path = f"{base}_{counter}{ext}"
            counter += 1
        return dest_path

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MoveFileApp()
    window.show()
    sys.exit(app.exec())
