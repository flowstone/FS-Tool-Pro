import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QGroupBox, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QLabel, \
    QFileDialog


class PreferencesAbout(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("配置文件存储位置")
        self.setGeometry(100, 100, 400, 150)

        # 创建QGroupBox
        group_box = QGroupBox("配置文件存储位置", self)

        # 创建布局
        main_layout = QVBoxLayout()
        group_box_layout = QHBoxLayout()

        # 第一行：标签 + 文本框
        self.path_label = QLabel("路径：", self)
        self.path_edit = QLineEdit(self)

        # 添加第一行（标签和文本框）和第二行（按钮）
        group_box_layout.addWidget(self.path_label)
        group_box_layout.addWidget(self.path_edit)
        group_box.setLayout(group_box_layout)


        # 设置按钮对齐方式
        button_layout = QHBoxLayout()
        # 第二行：按钮
        self.open_folder_btn = QPushButton("打开所在文件夹", self)
        button_layout.addWidget(self.open_folder_btn)
        button_layout.setAlignment(self.open_folder_btn, Qt.AlignLeft)

        right_button_layout = QHBoxLayout()
        self.open_btn = QPushButton("打开", self)
        self.change_btn = QPushButton("更改", self)

        right_button_layout.addWidget(self.open_btn)
        right_button_layout.addWidget(self.change_btn)

        # 将按钮的对齐设置为左对齐和右对齐
        right_button_layout.setAlignment(self.open_btn, Qt.AlignRight)
        right_button_layout.setAlignment(self.change_btn, Qt.AlignRight)

        button_layout.addLayout(right_button_layout)



        # 将QGroupBox添加到主布局
        main_layout.addWidget(group_box)
        main_layout.addLayout(button_layout)

        self.setLayout(main_layout)

        # 连接信号与槽函数
        self.open_folder_btn.clicked.connect(self.open_folder)
        self.open_btn.clicked.connect(self.open_file)
        self.change_btn.clicked.connect(self.change_path)

    def open_folder(self):
        path = self.path_edit.text()
        if path:
            # 打开文件夹
            QFileDialog.getExistingDirectory(self, "打开所在文件夹", path)

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "打开文件", self.path_edit.text())
        if file_path:
            self.path_edit.setText(file_path)

    def change_path(self):
        new_path = QFileDialog.getExistingDirectory(self, "选择新的路径")
        if new_path:
            self.path_edit.setText(new_path)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PreferencesAbout()
    window.show()
    sys.exit(app.exec_())
