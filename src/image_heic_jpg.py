import os
import sys

import pillow_heif
import whatimage
from PIL import Image, ImageOps
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog
from fs_base.message_util import MessageUtil
from fs_base.widget import TransparentTextBox, CustomProgressBar
from loguru import logger
from pillow_heif import register_heif_opener

from src.const.color_constants import BLUE, BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil

from src.widget.sub_window_widget import SubWindowWidget

# 注册HEIC文件 opener，使得PIL能够识别并打开HEIC格式文件，仅限V2方法使用
register_heif_opener()

class HeicToJpgApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IMAGE_HEIC_JPG} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_IMAGE_HEIC_JPG)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        self.setWindowFlags(self.windowFlags() | Qt.WindowType.MSWindowsFixedSizeDialogHint)
        self.setAcceptDrops(True)
        # self.setFixedHeight(200)
        # self.setFixedWidth(600)


        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))

        layout = QVBoxLayout()
        title_label = QLabel("批量HEIC转JPG")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)
        # 说明文本
        description_label = QLabel("说明：请选择HEIC文件所在的文件夹，系统将自动将其中的HEIC文件转换为JPG格式。")
        description_label.setFont(FontConstants.ITALIC_SMALL)
        description_label.setWordWrap(True)
        folder_path_label = QLabel("选择文件夹：")
        # 选择文件夹相关部件
        folder_path_layout = QHBoxLayout()
        self.folder_path_input = QLineEdit()
        self.folder_path_input.setObjectName("folder_path_input")

        browse_button = QPushButton("选择")
        browse_button.setObjectName("browse_button")
        browse_button.clicked.connect(self.browse_folder)

        folder_path_layout.addWidget(self.folder_path_input)
        folder_path_layout.addWidget(browse_button)

        # 操作按钮
        button_layout = QHBoxLayout()
        start_button = QPushButton("开始")
        start_button.clicked.connect(self.start_operation)


        # exit_button = QPushButton("退出")
        # exit_button.setObjectName("exit_button")
        # exit_button.clicked.connect(self.close)


        button_layout.addWidget(start_button)
        #button_layout.addWidget(exit_button)

        # 布局组合
        layout.addWidget(description_label)
        layout.addWidget(folder_path_label)

        layout.addLayout(folder_path_layout)

        layout.addLayout(button_layout)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        layout.addWidget(TransparentTextBox())
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
                MessageUtil.show_warning_message("拖入的不是有效文件夹！")

    def start_operation(self):
        logger.info("---- 开始执行操作 ----")
        folder_path = self.folder_path_input.text()


        if folder_path:
            logger.info("---- 有选择文件夹，开始执行操作 ----")
            self.setEnabled(False)  # 禁用按钮，防止多次点击
            self.worker = HeicToJpgAppThread(folder_path)
            self.worker.update_progress_signal.connect(self.progress_bar.update_progress)

            self.worker.finished_signal.connect(self.operation_finished)
            self.worker.error_signal.connect(self.operation_error)  # 连接异常信号处理方法
            self.worker.start()
            self.progress_bar.show()

        else:
            MessageUtil.show_warning_message("请选择要操作的文件夹！")

    def operation_finished(self):
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_success_message("移动文件完成！")

    def operation_error(self, error_msg):
        logger.error(f"出现异常：{error_msg}")
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_warning_message("遇到异常停止工作")




class HeicToJpgAppThread(QThread):
    finished_signal = Signal()
    error_signal = Signal(str)  # 新增信号，用于发送错误信息
    update_progress_signal = Signal(int)

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

    def heic_to_jpg_v2(self, folder_path):
        all_files = []
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                if file.endswith('.HEIC') or file.endswith('.heic'):
                    all_files.append(os.path.join(root, file))

        total_files = len(all_files)
        if total_files == 0:
            logger.info("没有找到任何 HEIC 文件")
            return

        for index, file_path in enumerate(all_files):
            try:
                image = Image.open(file_path)
                # 使用 exif_transpose 方法根据 EXIF 信息调整图像方向
                image = ImageOps.exif_transpose(image)
                file_name = os.path.splitext(os.path.basename(file_path))[0] + '.jpg'
                output_path = os.path.join(os.path.dirname(file_path), file_name)
                image.convert('RGB').save(output_path, 'JPEG')
                logger.info(f"{file_path} 已成功转换为 {output_path}")

                # 计算并发送进度
                progress = int((index + 1) / total_files * 100)
                self.update_progress_signal.emit(progress)

            except Exception as e:
                logger.error(f"转换失败：{file_path}，错误信息：{e}")
                continue

        logger.info("所有 HEIC 图片转换完成！")

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
    sys.exit(app.exec())