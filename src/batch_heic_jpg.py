import os
import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt,pyqtSignal, QThread

from src.widget.custom_progress_widget import CustomProgressBar
from src.widget.progress_widget import ProgressWidget

from PyQt5.QtWidgets import QMessageBox
from loguru import logger
from src.util.common_util import CommonUtil
from src.const.fs_constants import FsConstants
import whatimage
import pillow_heif
from PIL import Image,ImageOps
from pillow_heif import register_heif_opener
from src.const.color_constants import BLUE, BLACK
from src.const.font_constants import FontConstants
# 注册HEIC文件 opener，使得PIL能够识别并打开HEIC格式文件，仅限V2方法使用
register_heif_opener()

class HeicToJpgApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  pyqtSignal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info("---- 初始化HEIC转JPG ----")
        self.setWindowTitle(FsConstants.HEIC_JPG_WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() | Qt.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)
        self.setFixedHeight(300)
        self.setFixedWidth(600)


        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()
        title_label = QLabel("批量HEIC转JPG")
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet(f"color: {BLACK.name()};")
        title_label.setFont(FontConstants.H1)
        layout.addWidget(title_label)
        # 说明文本
        description_label = QLabel("说明：请选择HEIC文件所在的文件夹，系统将自动将其中的HEIC文件转换为JPG格式。")
        description_label.setStyleSheet(f"color: {BLUE.name()};")
        description_label.setWordWrap(True)

        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        folder_path_label = QLabel("选择文件夹：")
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setFixedWidth(300)
        self.folder_path_input.setObjectName("folder_path_input")
        self.folder_path_input.setStyleSheet("padding: 5px; border-radius: 4px; border: 1px solid #ccc;")

        browse_button = QPushButton("浏览")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(folder_path_label)
        folder_path_layout.addWidget(self.folder_path_input)
        folder_path_layout.addWidget(browse_button)

        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.setObjectName("start_button")
        start_button.clicked.connect(self.start_operation)


        # exit_button = QPushButton("退出")
        # exit_button.setObjectName("exit_button")
        # exit_button.clicked.connect(self.close)


        button_layout.addWidget(start_button)
        #button_layout.addWidget(exit_button)

        # 布局组合
        layout.addWidget(description_label)
        layout.addLayout(folder_path_layout)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        layout.addLayout(button_layout)

        self.setLayout(layout)



    def browse_folder(self):
        logger.info("---- 开始选择文件夹 ----")
        folder_path = QFileDialog.getExistingDirectory(self, "选择文件夹")
        self.folder_path_input.setText(folder_path)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():
            folder_path = event.mimeData().urls()[0].toLocalFile()
            if os.path.isdir(folder_path):
                self.folder_path_input.setText(folder_path)
            else:
                QMessageBox.warning(self, "警告", "拖入的不是有效文件夹！")

    def start_operation(self):
        logger.info("---- 开始执行操作 ----")
        folder_path = self.folder_path_input.text()


        if folder_path:
            logger.info("---- 有选择文件夹，开始执行操作 ----")
            self.setEnabled(False)  # 禁用按钮，防止多次点击
            self.progress_bar.set_range(0,0)
            self.worker = HeicToJpgAppThread(folder_path)
            self.worker.finished_signal.connect(self.operation_finished)
            self.worker.error_signal.connect(self.operation_error)  # 连接异常信号处理方法
            self.worker.start()
            self.progress_bar.show()

        else:
            QMessageBox.warning(self, "警告", "请选择要操作的文件夹！")

    def operation_finished(self):
        self.progress_bar.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "提示", "移动文件完成！")

    def operation_error(self, error_msg):
        logger.error(f"出现异常：{error_msg}")
        self.progress_bar.hide()
        self.setEnabled(True)
        QMessageBox.information(self, "警告", "遇到异常停止工作")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)



class HeicToJpgAppThread(QThread):
    finished_signal = pyqtSignal()
    error_signal = pyqtSignal(str)  # 新增信号，用于发送错误信息

    def __init__(self, folder_path):
        super().__init__()
        self.folder_path = folder_path

    def run(self):
        try:

            self.heic_to_jpg_v2(self.folder_path)
            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))  # 如果出现异常，发送异常信息

        # +++++ 最新方法 +++++
        # PIL导入Image
        # from PIL import Image,ImageOps
        # from pillow_heif import register_heif_opener
        # 注册HEIC文件 opener，使得PIL能够识别并打开HEIC格式文件
        # register_heif_opener()

    @staticmethod
    def heic_to_jpg_v2(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.HEIC') or file.endswith('.heic'):
                    file_path = os.path.join(root, file)
                    image = Image.open(file_path)
                    # 使用exif_transpose方法根据EXIF信息调整图像方向
                    image = ImageOps.exif_transpose(image)
                    file_name = file.split('.')[0] + '.jpg'
                    output_path = os.path.join(root, file_name)
                    image.convert('RGB').save(output_path, 'JPEG')
                    logger.info(f"{file_path} 已成功转换为 {output_path}")
        logger.info("所有HEIC图片转换完成！")

    # 创建文件夹，并移动到指定目录下
    # import whatimage
    # import pillow_heif
    # 但是个别HEIC图片无法识别
    @staticmethod
    def heic_to_jpg(folder_path):
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                with open(file_path, 'rb') as f:
                    file_data = f.read()
                    fmt = whatimage.identify_image(file_data)
                    if fmt == 'heic':
                        heif_file = pillow_heif.read_heif(file_path)
                        image = Image.frombytes(mode=heif_file.mode, size=heif_file.size, data=heif_file.data)
                        new_file_name = os.path.splitext(file)[0] + '.jpg'
                        new_file_path = os.path.join(root, new_file_name)
                        image.save(new_file_path, 'JPEG')
                        logger.info(f'已将 {file_path} 转换为 {new_file_path}')



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeicToJpgApp()
    window.show()
    sys.exit(app.exec_())