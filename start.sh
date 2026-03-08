#!/bin/bash
# 修仙模拟器启动脚本 (Linux/Mac)

echo "===================================="
echo "  修仙模拟器 v2.0"
echo "===================================="
echo ""

# 检查 Python 是否安装
if ! command -v python3 &> /dev/null; then
    echo "[错误] 未找到 Python，请先安装 Python 3.8+"
    exit 1
fi

echo "[信息] 启动游戏..."
echo ""

# 运行游戏
python3 -m cultivation "$@"
