#!/bin/bash

# ASCII 艺术字形式的 banner 图案，可以自行替换成你喜欢的样式
banner="
  _____   ____            _____                   _
 |  ___| / ___|          |_   _|   ___     ___   | |
 | |_    \___ \   _____    | |    / _ \   / _ \  | |
 |  _|    ___) | |_____|   | |   | (_) | | (_) | | |
 |_|     |____/            |_|    \___/   \___/  |_|
"

# 输出 banner 图案
echo "$banner"
echo "开始构建流体石头的工具箱应用程序..."

# 执行pyinstaller命令进行打包
pyinstaller --name "流体石头的工具箱" --onefile --window \
--add-data "F:/Workspace/PycharmProjects/fs-tool/.venv/Lib/site-packages/PyQt5/Qt5/bin;./PyQt5/Qt/bin" \
--add-data "F:/Workspace/PycharmProjects/fs-tool/.venv/Lib/site-packages/PyQt5/Qt5/plugins;./PyQt5/Qt/plugins" \
--add-data "resources;resources" \
--collect-all PyQt5 \
--icon=resources/app.ico \
./app.py

# 判断pyinstaller命令的执行结果，如果返回值为0表示成功，输出成功提示信息，否则输出失败提示信息
if [ $? -eq 0 ]; then
    echo "流体石头的工具箱应用程序构建成功！"
else
    echo "流体石头的工具箱应用程序构建失败，请检查相关错误信息。"
fi

# 输出结束提示信息，让整个执行过程有始有终，更清晰明了
echo "构建流程结束。"