import os
import sys

from PIL import Image
from PySide6.QtCore import Qt, Signal, QThread
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QApplication, QScrollArea, QWidget, QVBoxLayout, QPushButton, QLabel, QCheckBox, \
    QFileDialog, QHBoxLayout
from loguru import logger

from src.const.color_constants import BLACK
from src.const.font_constants import FontConstants
from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar


class ImageConvertApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal =  Signal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_IMAGE_CONVERT} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_IMAGE_CONVERT)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))


        # 用于存储上传的图片路径
        self.image_path = None

        # 主布局
        layout = QVBoxLayout()
        title_label = QLabel("图片格式转换")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setObjectName("app_title")
        layout.addWidget(title_label)


        # 上传图片按钮
        self.upload_button = QPushButton("上传图片")
        self.upload_button.setObjectName("browse_button")
        self.upload_button.clicked.connect(self.upload_image)
        layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # 图片预览区域
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setPixmap(QPixmap())  # 空图像预览
        self.image_label.setStyleSheet("border: 2px dashed #999999; padding: 10px; margin-top: 20px;")
        layout.addWidget(self.image_label)

        # 复选框框架
        self.checkbox_frame = QWidget(self)
        checkbox_layout = QVBoxLayout()  # 使用垂直布局
        self.checkbox_frame.setLayout(checkbox_layout)

        # 定义支持的目标格式
        self.target_formats = ["JPEG", "PNG", "GIF", "BMP", "WEBP", "ICO"]
        self.selected_formats = []

        # 创建复选框并添加到布局中
        for format in self.target_formats:
            checkbox = QCheckBox(format)
            checkbox.setStyleSheet("font-weight: normal;")
            checkbox.stateChanged.connect(lambda state, f=format: self.toggle_format(f, state))
            checkbox_layout.addWidget(checkbox)

        # 滚动区域（如果复选框过多）
        scroll_area = QScrollArea(self)
        scroll_area.setWidget(self.checkbox_frame)
        scroll_area.setWidgetResizable(True)
        layout.addWidget(scroll_area)

        # 按钮布局
        button_layout = QHBoxLayout()

        # 转换按钮
        self.convert_button = QPushButton("转换")
        self.convert_button.setEnabled(False)
        self.convert_button.clicked.connect(self.convert_image)
        button_layout.addWidget(self.convert_button)

        # 关闭按钮
        # self.close_button = QPushButton("关闭")
        # self.close_button.setObjectName("exit_button")
        # self.close_button.clicked.connect(self.close)
        # button_layout.addWidget(self.close_button)

        layout.addLayout(button_layout)
        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()
        layout.addWidget(self.progress_bar)
        self.setLayout(layout)



    def upload_image(self):
        logger.info("---- 开始上传图片 ----")
        self.image_path = QFileDialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.jpg *.png *.gif *.bmp *.webp *.ico)")[0]
        if self.image_path:
            logger.info(f"已上传图片: {self.image_path}")
            try:
                self.preview_image = Image.open(self.image_path)
                pixmap = QPixmap(self.image_path)
                pixmap = pixmap.scaled(FsConstants.PIC_CONVERSION_WINDOW_WIDTH, FsConstants.PIC_CONVERSION_WINDOW_WIDTH, Qt.AspectRatioMode.KeepAspectRatio,Qt.TransformationMode.SmoothTransformation)
                self.image_label.setPixmap(pixmap)
            except Exception as e:
                logger.error(f"显示图片时出错: {e}")

    def toggle_format(self, format, state):
        if state == 2:  # 表示选中状态（PyQt中选中为2，未选中为0）
            self.selected_formats.append(format)
        else:
            self.selected_formats.remove(format) if format in self.selected_formats else None
        logger.info(f"----{self.selected_formats}")
        # 根据是否有复选框被选中来更新转换按钮的状态
        if len(self.selected_formats) > 0:
            self.convert_button.setEnabled(True)
        else:
            self.convert_button.setEnabled(False)

    def convert_image(self):

        if not self.image_path:
            logger.warning("---- 请先上传图片! ----")
            MessageUtil.show_warning_message("请先上传图片!")
            return

        self.setEnabled(False)
        self.progress_bar.set_range(0,0)
        self.worker_thread = ImageConversionThread(self.image_path, self.selected_formats)
        self.worker_thread.finished_signal.connect(self.conversion_finished)
        self.worker_thread.error_signal.connect(self.conversion_error)
        self.worker_thread.start()
        self.progress_bar.show()

    def conversion_finished(self):
        logger.info("---- 图片转换完成 ----")
        self.progress_bar.hide()
        self.setEnabled(True)
        logger.info(
            f"图片已成功转换为所选格式，保存路径分别为: {[f'{os.path.splitext(self.image_path)[0]}.{f.lower()}' for f in self.selected_formats]}")
        MessageUtil.show_success_message("移动文件完成！")


    def conversion_error(self, error_msg):
        logger.error(f"转换图片时出错: {error_msg}")
        self.progress_bar.hide()
        self.setEnabled(True)
        MessageUtil.show_warning_message("遇到异常停止工作")

    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

class ImageConversionThread(QThread):
    finished_signal = Signal()
    error_signal = Signal(str)

    def __init__(self, image_path, selected_formats):
        super().__init__()
        self.image_path = image_path
        self.selected_formats = selected_formats

    def run(self):
        try:


            image = Image.open(self.image_path)
            for target_format in self.selected_formats:
                base_name, ext = os.path.splitext(self.image_path)
                new_image_path = f"{base_name}.{target_format.lower()}"
                if target_format == "JPEG":
                    image = image.convert('RGB')
                elif target_format == "ICO":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                    image.save(new_image_path, format='ICO')
                    continue
                elif target_format == "WEBP":
                    image = image.convert('RGB') if image.mode!= 'RGB' else image
                image.save(new_image_path)

            self.finished_signal.emit()
        except Exception as e:
            self.error_signal.emit(str(e))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ImageConvertApp()
    window.show()
    sys.exit(app.exec())