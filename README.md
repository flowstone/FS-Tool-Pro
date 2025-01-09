# FS Tool Pro
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![Python](https://img.shields.io/badge/python-3.9%2B-blue)
![PySide6](https://img.shields.io/badge/PySide-6.8.1%2B-orange)

一个轻量级的个人工具，基于 **PySide6** 构建，代码由ChatGPT、豆包生成，本人只是搬运工。

---

### 🌟 功能
* 透明时间
* 快捷便签
* 生成器工具
* 图片工具
* 文件工具
* HASH校验
* 网络工具
* 文件签名
* 快速发送
* ...

---

### 🖥️ 应用演示

<img src="https://raw.githubusercontent.com/flowstone/fs-tool-pro/main/resources/preview/preview_app_main.png" alt="应用截图" width="500px">
<img src="https://raw.githubusercontent.com/flowstone/fs-tool-pro/main/resources/preview/preview_app_float.png" alt="应用截图" width="90px">



---

### 🚀 快速开始

>干就完了，集帅们

#### 目录介绍
``` bash
.github/        # GitHub Actions
doc/            # 说明文档
resources/      # 资源文件 图片、字体、样式等
src/            # 源码
    ├── const/  # 常量
    ├── ui/     # 暂未使用
    ├── util/   # 工具代码
    ├── widget/ # 自定义控件
    ├── *.py    # 所有功能的Python文件
static/         # 静态资源 用于Flask服务
templates/      # 模板文件 用于Flask服务
tests/          # 测试代码
app.py          # 应用启动文件
build.ps1       # Win打包脚本
build.sh        # macOS打包脚本  
flask_server.py # Flask服务启动文件
requirements.txt# 依赖包
...
```

#### 添加功能
1. 在 `src` 目录下新建一个 `.py` 文件，编写功能代码
##### 添加子功能
在现有的功能下添加子功能，找到对应的功能文件，主界面功能的入口的命名规则为 `*_tool.py`,你只需要修改部分代码，如下：
``` python
 def add_tabs(self):
    self.tab_widget.addTab(IpInfoApp(), "网络信息")
    self.tab_widget.addTab(PortScannerApp(), "端口扫描")
    self.tab_widget.addTab(PortKillerApp(), "端口关闭") # 新添加的子功能
```
##### 添加新功能(主界面)
准备好应用的图片资源，放在 `resources/images/icon` 目录下，可以把路径地址写到常量文件`fs_constants.py`中，当然也可以在代码中写死，
只需要在`app_instance_config`中添加新代码即可，如下：
``` python
app_instance_config = [
        {
            "key": "desktop_clock", # 新功能的key
            "icon": FsConstants.APP_ICON_DESKTOP_CLOCK, # 图标路径，可以写死
            "title": FsConstants.APP_TITLE_DESKTOP_CLOCK, # 应用标题
            "class": DesktopClockSetting # 应用的类名
        },
        {
            "key": "stick_note",
            "icon": FsConstants.APP_ICON_STICK_NOTE,
            "title": FsConstants.APP_TITLE_STICK_NOTE,
            "class": StickyNoteApp
        },
        ]
```
上述代码中，json块的顺序即为应用的顺序，你可以根据自己的需求调整顺序，程序会根据这个配置生成应用的图标和标题。

---

### 🛠️ 未来计划
活下去...

---
### 📜 许可证

本项目使用 [Apache 2.0 许可证](https://github.com/flowstone/FS-Tool-Pro/blob/main/LICENSE)。  
您可以在符合许可证要求的情况下自由使用本项目代码。更多详情请参阅 [LICENSE 文件](https://github.com/flowstone/FS-Tool-Pro/blob/main/LICENSE)。

---

### 🙌 致谢

感谢以下开源库的支持：

- [PySide6](https://doc.qt.io/qtforpython-6/)
- [loguru](https://github.com/Delgan/loguru)
- [pyperclip](https://github.com/asweigart/pyperclip)

如果您觉得本项目有帮助，请记得点个 ⭐️！ 😊
