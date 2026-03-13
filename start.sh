#!/bin/bash

echo "========================================"
echo "   修仙模拟器 - 本地 Web 服务器"
echo "========================================"
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未检测到 Python3，请先安装 Python 3.8+"
    echo "安装方法：sudo apt-get install python3 或使用官方安装包"
    exit 1
fi

echo "[提示] Python 版本：$(python3 --version)"
echo ""

# 进入 web 目录
cd "$(dirname "$0")/web"

echo "[提示] 当前目录：$(pwd)"
echo ""
echo "========================================"
echo "   服务器即将启动"
echo "   访问地址：http://localhost:8080/game.html"
echo "   按 Ctrl+C 可停止服务器"
echo "========================================"
echo ""

# 启动服务器
python3 -m http.server 8080
