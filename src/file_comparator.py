import sys
import os
import hashlib

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (
    QApplication, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QLabel, QWidget, QComboBox,
    QMessageBox, QTextEdit
)
from PyQt5.QtCore import Qt, pyqtSignal, QThread

from src.util.common_util import CommonUtil
from src.const.color_constants import BLUE, BLACK
from src.const.font_constants import FontConstants
from src.widget.custom_progress_widget import CustomProgressBar


class CompareThread(QThread):
    update_signal = pyqtSignal(str)
    break_signal = pyqtSignal(str)
    done_signal = pyqtSignal(int, int)  # 返回比较结果，(相同文件数量, 不同文件数量)

    def __init__(self, source_directory, target_directory, method):
        super().__init__()
        self.source_directory = source_directory
        self.target_directory = target_directory
        self.method = method

    def run(self):
        """执行文件比较"""
        source_files = set(os.listdir(self.source_directory))
        target_files = set(os.listdir(self.target_directory))
        common_files = source_files.intersection(target_files)

        if not common_files:
            self.update_signal.emit("没有相同文件名的文件。")
            self.break_signal.emit("没有相同文件名的文件。")
            return

        total_same_files = 0
        total_diff_files = 0
        result = "文件比较结果:\n\n"

        for file_name in common_files:
            source_file_path = os.path.join(self.source_directory, file_name)
            target_file_path = os.path.join(self.target_directory, file_name)

            result += f"正在比较文件: {file_name}"

            if self.method == "文件大小比较":
                if self.compare_by_size(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  文件大小相同\n"
                else:
                    total_diff_files += 1
                    result += "  文件大小不匹配\n"

            elif self.method == "哈希算法比较":
                if self.compare_by_hash(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  哈希值相同\n"
                else:
                    total_diff_files += 1
                    result += "  哈希值不匹配\n"

            elif self.method == "逐字节比较":
                if self.compare_by_bytes(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  文件内容相同\n"
                else:
                    total_diff_files += 1
                    result += "  文件内容不匹配\n"

            elif self.method == "校验和比较":
                if self.compare_by_checksum(source_file_path, target_file_path):
                    total_same_files += 1
                    result += "  校验和相同\n"
                else:
                    total_diff_files += 1
                    result += "  校验和不匹配\n"

            self.update_signal.emit(result)  # 逐步更新UI

        self.done_signal.emit(total_same_files, total_diff_files)

    def compare_by_size(self, file1, file2):
        """通过文件大小比较"""
        return os.path.getsize(file1) == os.path.getsize(file2)

    def compare_by_hash(self, file1, file2):
        """通过哈希算法比较"""
        def file_hash(file_path):
            sha256_hash = hashlib.sha256()
            with open(file_path, "rb") as f:
                for byte_block in iter(lambda: f.read(4096), b""):
                    sha256_hash.update(byte_block)
            return sha256_hash.hexdigest()

        return file_hash(file1) == file_hash(file2)

    def compare_by_bytes(self, file1, file2):
        """逐字节比较"""
        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            while True:
                byte1 = f1.read(4096)
                byte2 = f2.read(4096)
                if byte1 != byte2:
                    return False
                if not byte1:
                    return True

    def compare_by_checksum(self, file1, file2):
        """通过校验和比较"""
        def file_checksum(file_path):
            checksum = 0
            with open(file_path, "rb") as f:
                while chunk := f.read(4096):
                    checksum ^= hash(chunk)
            return checksum

        return file_checksum(file1) == file_checksum(file2)


class FileComparatorApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.setWindowTitle("文件比较")
        self.setFixedSize(800, 600)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()
        title_label = QLabel("批量文件比较")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)

        self.label = QLabel("请选择源目录和目标目录进行文件比较")
        self.label.setStyleSheet(f"color: {BLUE.name()};")
        layout.addWidget(self.label)

        self.source_label = QLabel("源目录: 未选择")
        layout.addWidget(self.source_label)

        self.target_label = QLabel("目标目录: 未选择")
        layout.addWidget(self.target_label)

        button_layout = QHBoxLayout()
        self.source_button = QPushButton("选择源目录")
        self.source_button.setObjectName("browse_button")
        self.source_button.clicked.connect(self.select_source_directory)
        button_layout.addWidget(self.source_button)

        self.target_button = QPushButton("选择目标目录")
        self.target_button.setObjectName("browse_button")
        self.target_button.clicked.connect(self.select_target_directory)
        button_layout.addWidget(self.target_button)

        layout.addLayout(button_layout)

        self.method_label = QLabel("请选择比较方法:")
        layout.addWidget(self.method_label)

        self.method_combo = QComboBox()
        self.method_combo.addItems(["文件大小比较", "哈希算法比较", "逐字节比较", "校验和比较"])
        layout.addWidget(self.method_combo)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        self.compare_button = QPushButton("开始比较")
        self.compare_button.setObjectName("start_button")
        self.compare_button.clicked.connect(self.start_comparison)
        layout.addWidget(self.compare_button)

        self.result_text = QTextEdit()
        self.result_text.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #388E3C;
                border-radius: 5px;
                padding: 10px;
                font-size: 14px;
            }
            QTextEdit:read-only {
                background-color: #f9f9f9;
            }
        """)
        self.result_text.setReadOnly(True)
        layout.addWidget(self.result_text)
        self.setLayout(layout)

        self.source_directory = None
        self.target_directory = None

    def select_source_directory(self):
        """选择源目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择源目录")
        if directory:
            self.source_directory = directory
            self.source_label.setText(f"源目录: {directory}")

    def select_target_directory(self):
        """选择目标目录"""
        directory = QFileDialog.getExistingDirectory(self, "选择目标目录")
        if directory:
            self.target_directory = directory
            self.target_label.setText(f"目标目录: {directory}")

    def start_comparison(self):
        """开始比较文件"""
        if not self.source_directory or not self.target_directory:
            QMessageBox.warning(self, "警告", "请先选择源目录和目标目录！")
            return
        self.compare_button.setEnabled(False)
        self.progress_bar.set_range(0,0)
        method = self.method_combo.currentText()
        self.compare_thread = CompareThread(self.source_directory, self.target_directory, method)
        self.compare_thread.update_signal.connect(self.update_result)
        self.compare_thread.done_signal.connect(self.display_summary)
        self.compare_thread.break_signal.connect(self.break_summary)
        self.compare_thread.start()
        self.progress_bar.show()

    def update_result(self, result):
        """更新结果"""
        self.result_text.setText(result)

    def break_summary(self, result):
        """中断结果"""
        self.compare_button.setEnabled(True)
        self.progress_bar.hide()

    def display_summary(self, same_count, diff_count):
        """显示比较总结"""
        summary = f"相同文件数量: {same_count} 个文件\n"
        summary += f"不同文件数量: {diff_count} 个文件\n"
        self.result_text.append(summary)
        self.compare_button.setEnabled(True)
        self.progress_bar.hide()

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = FileComparatorApp()
    window.show()
    sys.exit(app.exec_())
