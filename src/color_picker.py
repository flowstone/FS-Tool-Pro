import sys
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QPixmap, QColor, QIcon
from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QFileDialog, QGraphicsView, QGraphicsScene
from loguru import logger

from src.const.fs_constants import FsConstants
from src.util.common_util import CommonUtil
from src.widget.sub_window_widget import SubWindowWidget


class CustomGraphicsView(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.color_callback = None  # 用于设置颜色回调函数
        self.double_click_callback = None  # 设置双击回调函数

    def set_color_callback(self, callback):
        """设置颜色回调函数"""
        self.color_callback = callback

    def set_double_click_callback(self, callback):
        """设置双击回调函数"""
        self.double_click_callback = callback

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.scene():
            # 将鼠标点击位置映射到场景中的位置
            scene_pos = self.mapToScene(event.position().toPoint())
            if self.color_callback:
                self.color_callback(scene_pos)
        super().mousePressEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.scene():
            # 将鼠标双击位置映射到场景中的位置
            scene_pos = self.mapToScene(event.position().toPoint())
            if self.double_click_callback:
                self.double_click_callback(scene_pos)
        super().mouseDoubleClickEvent(event)


class ColorPickerApp(SubWindowWidget):

    def __init__(self):
        super().__init__()
        # 保存图片的原始 Pixmap 和缩放后的 Pixmap
        self.original_pixmap = None
        self.scaled_pixmap = None
        self.init_ui()

    def init_ui(self):
        logger.info(f"---- 初始化{FsConstants.WINDOW_TITLE_COLOR_PICKER} ----")
        self.setWindowTitle(FsConstants.WINDOW_TITLE_COLOR_PICKER)
        self.setWindowIcon(QIcon(CommonUtil.get_ico_full_path()))
        self.setFixedSize(600, 400)
        layout = QVBoxLayout()

        # 显示选中的颜色
        self.color_label = QLabel(self)
        self.color_label.setText("选择的颜色: None")
        self.color_label.setFixedHeight(30)
        layout.addWidget(self.color_label)

        # 按钮加载图片
        load_button = QPushButton("加载图片", self)
        load_button.clicked.connect(self.load_image)
        layout.addWidget(load_button)

        # 设置自定义画布（用于显示图片）
        self.scene = QGraphicsScene(self)
        self.view = CustomGraphicsView(self)
        self.view.setScene(self.scene)
        self.view.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.view.setRenderHint(self.view.renderHints())
        layout.addWidget(self.view)

        # 绑定鼠标点击颜色回调
        self.view.set_color_callback(self.get_color_on_click)
        # 绑定鼠标双击回调
        self.view.set_double_click_callback(self.copy_color_on_double_click)

        self.setLayout(layout)



    def resizeEvent(self, event):
        """在窗口调整大小时，让图片自适应窗口大小"""
        if self.original_pixmap:
            self.update_image_scaling()
        super().resizeEvent(event)

    def load_image(self):
        """加载图片"""
        file_dialog = QFileDialog(self)
        file_path, _ = file_dialog.getOpenFileName(self, "选择图片", "", "图片文件 (*.png *.jpg *.jpeg *.bmp)")

        if file_path:
            # 加载图片并保存原始 Pixmap
            self.original_pixmap = QPixmap(file_path)
            self.update_image_scaling()

    def update_image_scaling(self):
        """根据窗口大小调整图片的显示比例"""
        view_size = self.view.size()
        if self.original_pixmap:
            self.scaled_pixmap = self.original_pixmap.scaled(
                view_size.width(),
                view_size.height(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            self.scene.clear()
            self.scene.addPixmap(self.scaled_pixmap)
            self.view.setScene(self.scene)
            self.view.setSceneRect(self.scene.itemsBoundingRect())

    def get_color_on_click(self, scene_pos):
        """获取点击位置的颜色"""
        if self.scaled_pixmap:
            mapped_pos = scene_pos.toPoint()
            if self.scaled_pixmap.rect().contains(mapped_pos):
                # 根据点击位置获取颜色
                color = self.scaled_pixmap.toImage().pixelColor(mapped_pos)
                hex_color = color.name()  # 获取颜色的 HEX 值
                self.color_label.setText(f"选择的颜色: {hex_color}")
                logger.info(f"选择的颜色: {hex_color}")
                self.color_label.setStyleSheet(f"background-color: {hex_color};")
            else:
                self.color_label.setText("选择的颜色: None")
                logger.info("选择的颜色: None")

    def copy_color_on_double_click(self, scene_pos):
        """双击时复制颜色到剪贴板"""
        if self.scaled_pixmap:
            mapped_pos = scene_pos.toPoint()
            if self.scaled_pixmap.rect().contains(mapped_pos):
                # 获取颜色并复制到剪贴板
                color = self.scaled_pixmap.toImage().pixelColor(mapped_pos)
                hex_color = color.name()  # 获取颜色的 HEX 值
                clipboard = QApplication.clipboard()
                clipboard.setText(hex_color)  # 将颜色复制到剪贴板

                # 更新标签并提示用户
                self.color_label.setText(f"颜色已复制: {hex_color}")
                logger.info(f"颜色已复制: {hex_color}")
                self.color_label.setStyleSheet(f"background-color: {hex_color};")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ColorPickerApp()
    window.show()
    sys.exit(app.exec())
