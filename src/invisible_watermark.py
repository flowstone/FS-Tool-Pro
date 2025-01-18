from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog, QMessageBox, QHBoxLayout, QProgressBar
)
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtCore import Qt, QThread, Signal
import numpy as np
from PIL import Image
import os
from loguru import logger

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.util.message_util import MessageUtil
from src.widget.custom_progress_widget import CustomProgressBar
from src.widget.transparent_textbox_widget import TransparentTextBox


class WatermarkThread(QThread):
    progress = Signal(int)
    finished = Signal(bool, str)

    def __init__(self, mode, image_path, watermark_text=""):
        super().__init__()
        self.mode = mode
        self.image_path = image_path
        self.watermark_text = watermark_text

    def run(self):
        try:
            if self.mode == "embed":
                # 嵌入水印
                img = Image.open(self.image_path).convert("RGB")
                img_array = np.array(img)
                watermark_bin = ''.join(format(ord(c), '08b') for c in self.watermark_text)
                watermark_length = len(watermark_bin)
                length_bin = f"{watermark_length:016b}"
                full_watermark_bin = length_bin + watermark_bin

                if len(full_watermark_bin) > img_array.size:
                    self.finished.emit(False, "图片大小不足以嵌入水印！")
                    return

                flat_img = img_array.flatten().astype(np.int16)
                for i, bit in enumerate(full_watermark_bin):
                    flat_img[i] = (flat_img[i] & ~1) | int(bit)
                    self.progress.emit(int((i + 1) / len(full_watermark_bin) * 100))

                flat_img = np.clip(flat_img, 0, 255).astype(np.uint8)
                watermarked_img = flat_img.reshape(img_array.shape)
                output_path = os.path.join(
                    os.path.dirname(self.image_path),
                    f"watermarked_{os.path.basename(self.image_path)}"
                )
                Image.fromarray(watermarked_img).save(output_path)
                self.finished.emit(True, f"隐水印图片已生成：\n{output_path}")

            elif self.mode == "extract":
                # 提取水印
                img = Image.open(self.image_path).convert("RGB")
                img_array = np.array(img)
                flat_img = img_array.flatten()
                length_bits = ''.join(str(flat_img[i] & 1) for i in range(16))
                watermark_length = int(length_bits, 2)

                if watermark_length <= 0 or watermark_length > (flat_img.size - 16):
                    self.finished.emit(False, "未检测到有效的隐水印！")
                    return

                watermark_bits = ''.join(str(flat_img[i] & 1) for i in range(16, 16 + watermark_length))
                watermark_chars = [
                    chr(int(watermark_bits[i:i + 8], 2))
                    for i in range(0, len(watermark_bits), 8)
                ]
                extracted_text = ''.join(watermark_chars)
                self.finished.emit(True, f"隐水印内容：{extracted_text}")

        except Exception as e:
            self.finished.emit(False, f"操作失败：{e}")


class InvisibleWatermarkApp(QWidget):
    # 定义一个信号，在窗口关闭时触发
    closed_signal = Signal()
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_INVISIBLE_WATERMARK} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_INVISIBLE_WATERMARK)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        # UI 元素
        self.label_image = QLabel("上传图片预览", self)
        self.label_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_image.setFixedHeight(200)

        self.button_upload = QPushButton("上传图片", self)
        self.input_watermark = QLineEdit(self)
        self.input_watermark.setPlaceholderText("请输入隐水印文字")

        self.progress_bar = CustomProgressBar()
        self.progress_bar.hide()

        button_layout = QHBoxLayout()
        self.button_embed = QPushButton("嵌入隐水印", self)
        self.button_extract = QPushButton("提取隐水印", self)
        button_layout.addWidget(self.button_embed)
        button_layout.addWidget(self.button_extract)

        # 布局
        layout = QVBoxLayout()
        layout.addWidget(self.label_image)
        layout.addWidget(self.button_upload)
        layout.addWidget(QLabel("隐水印文字："))
        layout.addWidget(self.input_watermark)
        layout.addLayout(button_layout)
        layout.addWidget(self.progress_bar)
        layout.addWidget(TransparentTextBox())
        self.setLayout(layout)

        # 绑定事件
        self.button_upload.clicked.connect(self.upload_image)
        self.button_embed.clicked.connect(self.start_embed_watermark)
        self.button_extract.clicked.connect(self.start_extract_watermark)

        # 初始化属性
        self.image_path = None

    def upload_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "选择图片文件", "", "图像文件 (*.png *.bmp)"
        )
        if file_path:
            self.image_path = file_path
            pixmap = QPixmap(file_path)
            self.label_image.setPixmap(pixmap.scaled(self.label_image.size(), Qt.AspectRatioMode.KeepAspectRatio))
            MessageUtil.show_success_message("图片上传成功！")

    def start_embed_watermark(self):
        if not self.image_path:
            MessageUtil.show_warning_message("请先上传图片！")
            return

        watermark_text = self.input_watermark.text().strip()
        if not watermark_text:
            MessageUtil.show_warning_message("请输入隐水印文字！")
            return
        self.button_embed.setEnabled(False)
        self.thread = WatermarkThread("embed", self.image_path, watermark_text)
        self.thread.progress.connect(self.progress_bar.update_progress)
        self.thread.finished.connect(self.on_operation_finished)
        self.thread.start()
        self.progress_bar.show()

    def start_extract_watermark(self):
        if not self.image_path:
            MessageUtil.show_warning_message("请先上传图片！")
            return

        self.button_extract.setEnabled(False)
        self.thread = WatermarkThread("extract", self.image_path)
        self.thread.progress.connect(self.progress_bar.update_progress)
        self.thread.finished.connect(self.on_operation_finished)
        self.thread.start()
        self.progress_bar.show()

    def on_operation_finished(self, success, message):
        self.progress_bar.hide()
        self.button_embed.setEnabled(True)
        self.button_extract.setEnabled(True)

        if success:
            MessageUtil.show_success_message(message)
        else:
            MessageUtil.show_error_message(message)
    def closeEvent(self, event):
        # 在关闭事件中发出信号
        self.closed_signal.emit()
        super().closeEvent(event)

if __name__ == "__main__":
    app = QApplication([])

    window = InvisibleWatermarkApp()
    window.show()

    app.exec()
