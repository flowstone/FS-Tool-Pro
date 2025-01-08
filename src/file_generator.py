import csv
import json
import os
import random
import string
import sys

from PIL import Image
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QVBoxLayout, QLineEdit, QPushButton, QFileDialog, QLabel, \
    QWidget, QComboBox, QHBoxLayout
from loguru import logger

from src.const.color_constants import BLACK, BLUE
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar


class FileGenerationThread(QThread):
    # Signals to communicate with the main thread
    update_progress_signal = Signal(str)
    file_generated_signal = Signal(int, str)
    finished_signal = Signal()

    def __init__(self, folder_path, file_count, file_size, file_type):
        super().__init__()
        self.folder_path = folder_path
        self.file_count = file_count
        self.file_size = file_size
        self.file_type = file_type

    def run(self):
        try:
            for i in range(self.file_count):
                self.update_progress_signal.emit(f"生成文件 {i + 1}...")
                if self.file_type == "文本文件":
                    self.generate_text_file(i + 1)
                elif self.file_type == "图片文件":
                    self.generate_image_file(i + 1)
                elif self.file_type == "JSON文件":
                    self.generate_json_file(i + 1)
                elif self.file_type == "CSV文件":
                    self.generate_csv_file(i + 1)
                self.file_generated_signal.emit(i + 1, self.file_type)
            self.finished_signal.emit()
        except Exception as e:
            logger.error(f"生成文件失败：{str(e)}")
            self.update_progress_signal.emit(f"生成文件失败：{str(e)}")

    def generate_text_file(self, index):
        """生成文本文件"""
        file_name = f"file_{index}.txt"
        file_path = os.path.join(self.folder_path, file_name)
        with open(file_path, "w", encoding="utf-8") as f:
            random_content = self.generate_random_content(self.file_size)
            f.write(random_content)

    def generate_image_file(self, index):
        """生成图片文件"""
        file_name = f"file_{index}.png"
        file_path = os.path.join(self.folder_path, file_name)
        width = int(self.file_size ** 0.5)
        height = int(self.file_size / width)
        image = Image.new('RGB', (width, height), color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
        image.save(file_path)

    def generate_json_file(self, index):
        """生成JSON文件"""
        file_name = f"file_{index}.json"
        file_path = os.path.join(self.folder_path, file_name)
        data = {"id": index, "name": f"Random File {index}", "content": self.generate_random_content(self.file_size)}
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

    def generate_csv_file(self, index):
        """生成CSV文件"""
        file_name = f"file_{index}.csv"
        file_path = os.path.join(self.folder_path, file_name)
        headers = ["ID", "Name", "Content"]
        rows = [[index, f"Random File {index}", self.generate_random_content(self.file_size)]]
        with open(file_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            writer.writerows(rows)

    def generate_random_content(self, size):
        """生成指定大小的随机内容"""
        characters = string.ascii_letters + string.digits + string.punctuation
        random_content = ''.join(random.choice(characters) for _ in range(size))
        return random_content


class FileGeneratorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = Signal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.folder_path = None
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_FILE_GENERATOR} ----")

        self.setWindowTitle(FsConstants.WINDOW_TITLE_FILE_GENERATOR)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        #self.setFixedSize(750, 400)
        self.setFixedHeight(400)
        self.setAcceptDrops(True)

        layout = QVBoxLayout()
        title_label = QLabel("批量生成文件")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)
        # 应用说明
        description_label = QLabel("批量文件生成工具，支持选择目录、设置文件数量、大小及类型")
        description_label.setFont(FontConstants.ITALIC_SMALL)
        description_label.setWordWrap(True)
        layout.addWidget(description_label)

        output_folder_label = QLabel("输出目录")
        layout.addWidget(output_folder_label)
        browse_layout = QHBoxLayout()

        self.folder_path_entry = QLineEdit()
        self.folder_path_entry.setPlaceholderText("请选择要生成文件的目录")
        self.select_folder_button = QPushButton("选择")
        self.select_folder_button.setObjectName("browse_button")
        self.select_folder_button.clicked.connect(self.select_folder)
        browse_layout.addWidget(self.folder_path_entry)
        browse_layout.addWidget(self.select_folder_button)
        layout.addLayout(browse_layout)

        self.file_count_label = QLabel("文件数量：")
        layout.addWidget(self.file_count_label)
        self.file_count_input = QLineEdit()
        self.file_count_input.setPlaceholderText("请输入文件数量")
        layout.addWidget(self.file_count_input)

        self.file_size_label = QLabel("文件大小 (KB)：")
        layout.addWidget(self.file_size_label)
        self.file_size_input = QLineEdit()
        self.file_size_input.setPlaceholderText("请输入每个文件的大小")
        layout.addWidget(self.file_size_input)

        self.file_type_label = QLabel("文件类型：")
        layout.addWidget(self.file_type_label)
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["文本文件", "图片文件", "JSON文件", "CSV文件"])
        layout.addWidget(self.file_type_combo)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()
        self.generate_button = QPushButton("生成文件")
        self.generate_button.clicked.connect(self.start_file_generation)
        button_layout.addWidget(self.generate_button)


        layout.addLayout(button_layout)
        self.setLayout(layout)

    def select_folder(self):
        self.folder_path = QFileDialog.getExistingDirectory(self, "选择输出目录")
        logger.info(f"选择的输出目录：{self.folder_path}")
        self.folder_path_entry.setText(self.folder_path)

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
    def start_file_generation(self):
        file_count = self.file_count_input.text()
        file_size = self.file_size_input.text()
        if not file_count.isdigit() or not file_size.isdigit():
            MessageUtil.show_warning_message("请输入有效的文件数量和文件大小！")
            return

        file_count = int(file_count)
        file_size = int(file_size) * 1024  # 转换为字节

        if file_count <= 0 or file_size <= 0:
            MessageUtil.show_warning_message("文件数量和文件大小必须大于零！")
            return

        if not self.folder_path:
            MessageUtil.show_warning_message("请先选择输出目录！")
            return

        file_type = self.file_type_combo.currentText()
        self.generate_button.setEnabled(False)
        self.progress_bar.set_range(0,0)
        self.thread = FileGenerationThread(self.folder_path, file_count, file_size, file_type)
        self.thread.update_progress_signal.connect(self.update_progress)
        self.thread.file_generated_signal.connect(self.file_generated)
        self.thread.finished_signal.connect(self.file_generation_finished)
        self.thread.start()
        self.progress_bar.show()

    def update_progress(self, message):
        logger.info(message)

    def file_generated(self, index, file_type):
        logger.info(f"第 {index} 个 {file_type} 文件已生成")

    def file_generation_finished(self):
        self.generate_button.setEnabled(True)
        self.progress_bar.hide()
        MessageUtil.show_success_message("文件生成完成！")


    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileGeneratorApp()
    window.show()
    sys.exit(app.exec())
