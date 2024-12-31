# FS Tool


### 脚本

#### 开始

在项目根目录下运行脚本
``` bash
pyinstaller --name "流体石头的工具箱" --onefile  --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin" --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\plugins;./PyQt5/Qt/plugins" --add-data "resources;resources" --add-data "config.json;." --collect-all PyQt5 --icon=resources/app.ico .\app.py
pip install -r requirements.txt
```

##### 1.打包Tkinter脚本
``` bash
pyinstaller --name "应用名" --onefile --window --icon=clock.ico 程序脚本.py
```

##### 2.打包PyQt脚本
``` bash
# WIN
pyinstaller --name "FS-Tool" --onefile  --window --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin" --add-data "F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\plugins;./PyQt5/Qt/plugins" --add-data "resources:resources" --add-data "config.json:." --collect-all PyQt5 --icon=resources/app.ico .\app.py
# MacOS
# pyinstaller --name "流体石头的工具箱" --onefile  --window  --add-data "/Users/simonxue/Code/PycharmProjects/FS-Tool/.venv/lib/python3.9/site-packages/PyQt5/Qt5:./PyQt5/Qt" --add-data "/Users/simonxue/Code/PycharmProjects/FS-Tool/.venv/lib/python3.9/site-packages/PyQt5/Qt5/plugins:./PyQt5/Qt/plugins" --add-data "resources:resources" --add-data "config.json:."  --icon=resources/app.ico ./app.py
pyinstaller --name "FS-Tool" --onefile  --window   --add-data "resources:resources" --add-data "config.json:." --icon=resources/app.ico ./app.py
```

###### 说明

``` bash 
F:\Workspace\PycharmProjects\fs-tool\.venv\Lib\site-packages\PyQt5\Qt5\bin;./PyQt5/Qt/bin
源PyQt5的目录:exe包中的目标路径
```

##### 预览
1. 应用图标

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-logo.png)

2. 应用界面

![老的界面](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-main-window.png)

![新的界面](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/1.png)


3. 关闭应用窗口，屏幕右上角会有悬浮球

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-mini.png)

4. 任务栏托盘

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/app-menu-bar.png)

5. 欢迎预览

![](https://raw.githubusercontent.com/flowstone/fs-tool/release/resources/preview/start-work.gif)


##### 备注
Chrome浏览器指定版本**131.0.6778.69**

**下载地址**
* https://pan.quark.cn/s/e3e92f0b8882
* https://caiyun.139.com/m/i?2i3pdpZu9b6jp  提取码:hk1n  
* https://drive.google.com/drive/folders/1PZUGmGvWMDzJEwF05vPtmo0BVk_q4FnX?usp=sharing
* https://www.dropbox.com/scl/fo/9taonyyqpx9u5trdhwssq/AIyi5on3cviaXjUANJnEv3g?rlkey=f5h9a4b10qvqzyrjtzte9kcf7&st=y80qblrx&dl=0