import sys
import os

from PyQt5.QtWidgets import QApplication, QGroupBox, QRadioButton, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QThread
from loguru import logger

from src.const.color_constants import BLACK
from src.util.common_util import CommonUtil
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.widget.custom_progress_widget import CustomProgressBar
from src.widget.progress_widget import ProgressWidget

class RenameCustomApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  pyqtSignal()
    def __init__(self, parent_self):
        super().__init__()
        self.check_type_text = None
        self.parent_self = parent_self
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化文件名批量修改工具 ----")
        self.setWindowTitle(FsConstants.FILE_RENAMER_WINDOW_TITLE)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)


        layout = QVBoxLayout()
        title_label = QLabel("批量修改文件/文件夹名")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)
        # 创建第一个单选按钮组（文件类型）
        group_box = QGroupBox('*文件类型')
        radio_btn_layout = QHBoxLayout()

        # 创建两个单选按钮
        self.file_rbtn = QRadioButton('文件')
        self.folder_rbtn = QRadioButton('文件夹')
        self.check_type_text = self.file_rbtn.text()
        self.file_rbtn.setChecked(True)  # 默认选中选项1
        self.file_rbtn.toggled.connect(self.radio_btn_toggled)
        self.folder_rbtn.toggled.connect(self.radio_btn_toggled)

        radio_btn_layout.addWidget(self.file_rbtn)
        radio_btn_layout.addWidget(self.folder_rbtn)
        group_box.setLayout(radio_btn_layout)
        layout.addWidget(group_box)



        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        self.folder_path_label = QLabel("*选择文件夹：")
        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setFixedWidth(300)
        self.folder_path_entry.setObjectName("folder_path_input")

        self.browse_button = QPushButton("浏览")
        self.browse_button.setObjectName("browse_button")
        self.browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(self.folder_path_label)
        folder_path_layout.addWidget(self.folder_path_entry)
        folder_path_layout.addWidget(self.browse_button)
        layout.addLayout(folder_path_layout)

        # 文件名前缀输入部件
        prefix_layout = QHBoxLayout()
        self.prefix_label = QLabel("文件名前缀：")
        self.prefix_entry = QLineEdit()

        prefix_layout.addWidget(self.prefix_label)
        prefix_layout.addWidget(self.prefix_entry)
        layout.addLayout(prefix_layout)

        # 文件名后缀输入部件
        suffix_layout = QHBoxLayout()
        self.suffix_label = QLabel("文件名后缀：")
        self.suffix_entry = QLineEdit()

        suffix_layout.addWidget(self.suffix_label)
        suffix_layout.addWidget(self.suffix_entry)
        layout.addLayout(suffix_layout)

        # 查找字符输入部件
        char_to_find_layout = QHBoxLayout()
        self.char_to_find_label = QLabel("查找字符：")
        self.char_to_find_entry = QLineEdit()

        char_to_find_layout.addWidget(self.char_to_find_label)
        char_to_find_layout.addWidget(self.char_to_find_entry)
        layout.addLayout(char_to_find_layout)

        # 替换字符输入部件
        replace_char_layout = QHBoxLayout()
        self.replace_char_label = QLabel("替换字符：")
        self.replace_char_entry = QLineEdit()

        replace_char_layout.addWidget(self.replace_char_label)
        replace_char_layout.addWidget(self.replace_char_entry)
        layout.addLayout(replace_char_layout)

        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        # 操作按钮
        button_layout = QHBoxLayout()
        self.start_button = QPushButton("开始")
        self.start_button.setObjectName("start_button")
        self.start_button.clicked.connect(self.start_operation)


        # self.exit_button = QPushButton("退出")
        # self.exit_button.setObjectName("exit_button")
        # self.exit_button.clicked.connect(self.close)


        button_layout.addWidget(self.start_button)
        # button_layout.addWidget(self.exit_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)




    # 文件类型Radio
    def radio_btn_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.check_type_text = radio_button.text()
            logger.info(f'当前选中：{radio_button.text()}')

    def browse_folder(self):
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
                QMessageBox.warning(self, "警告", "拖入的不是有效文件夹！")

    def start_operation(self):

        folder_path = self.folder_path_entry.text()
        prefix = self.prefix_entry.text()
        suffix = self.suffix_entry.text()
        char_to_find = self.char_to_find_entry.text()
        replace_char = self.replace_char_entry.text()

        if folder_path:
            self.setEnabled(False)
            self.progress_bar.set_range(0,0)

            self.worker_thread = FileRenameThread(folder_path, prefix, suffix, char_to_find, replace_char,
                                                  self.check_type_text)
            self.worker_thread.finished_signal.connect(self.operation_finished)
            self.worker_thread.error_signal.connect(self.operation_error)
            self.worker_thread.start()
            self.progress_bar.show()

        else:
            QMessageBox.warning(self, "警告", "请选择要修改的文件夹！")
            logger.warning("请选择要修改的文件夹")

    def operation_finished(self):
        logger.info("---- 操作完成 ----")
        self.progress_bar.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "提示", "批量改名完成！")

    def operation_error(self, error_msg):
        logger.error(f"出现异常：{error_msg}")
        self.progress_bar.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "警告", "遇到异常停止工作")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

class FileRenameThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)

    def __init__(self, folder_path, prefix, suffix, char_to_find, replace_char, check_type_text):
        super().__init__()
        self.folder_path = folder_path
        self.prefix = prefix
        self.suffix = suffix
        self.char_to_find = char_to_find
        self.replace_char = replace_char
        self.check_type_text = check_type_text


    def run(self):
        try:

            if self.check_type_text == "文件":
                logger.info(f"你选择类型是:{FsConstants.FILE_RENAMER_TYPE_FILE}")
                self.rename_files()
            else:
                logger.info(f"你选择的类型是：{FsConstants.FILE_RENAMER_TYPE_FOLDER}")
                self.rename_folder()


            self.finished_signal.emit()
        except OSError as e:
            self.error_signal.emit(str(e))

    def rename_files(self):
        # 遍历文件夹下的文件名

        for filename in os.listdir(self.folder_path):
            old_path = os.path.join(self.folder_path, filename)
            # 判断是否是文件
            if os.path.isfile(old_path):
                new_filename = f"{self.prefix}{filename}{self.suffix}"
                # 判断是否需要进行文件替换操作
                if self.char_to_find and self.replace_char:
                    # 替换字符
                    new_filename = new_filename.replace(self.char_to_find, self.replace_char)
                new_path = os.path.join(self.folder_path, new_filename)
                os.rename(old_path, new_path)


    def rename_folder(self):

        for dir_name in os.listdir(self.folder_path):
            old_path = os.path.join(self.folder_path, dir_name)
            if os.path.isdir(old_path):
                new_folder_name = f"{self.prefix}{dir_name}{self.suffix}"
                # 判断是否需要进行文件替换操作
                if self.char_to_find and self.replace_char:
                    # 替换字符
                    new_folder_name = new_folder_name.replace(self.char_to_find, self.replace_char)
                new_path = os.path.join(self.folder_path, new_folder_name)
                os.rename(old_path, new_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RenameCustomApp()
    window.show()
    sys.exit(app.exec_())