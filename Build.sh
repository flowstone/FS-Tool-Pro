#!/bin/bash

# 默认任务为 "build"
TASK=${1:-build}

# 构建函数
build_fstool_pro() {
    echo "Building FS-Tool-Pro..."
    python -m nuitka --show-progress --assume-yes-for-downloads app.py
}

# 清理函数
clean_fstool_pro() {
    echo "Cleaning..."
    rm -rf app.exe ./app.build/ ./app.dist/ ./app.onefile-build/
}

# 任务切换
case "${TASK,,}" in
    build)
        build_fstool_pro
        ;;
    clean)
        clean_fstool_pro
        ;;
    *)
        echo "Unknown task: $TASK"
        echo "Available tasks: build, clean"
        ;;
esac
