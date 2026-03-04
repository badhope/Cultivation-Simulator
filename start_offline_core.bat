@echo off

rem 修仙模拟器 - 离线核心程序启动脚本
echo 修仙模拟器 - 离线核心程序
echo =========================
echo.

rem 检查Python是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo 错误: Python未安装或未添加到环境变量
    echo 请先安装Python 3.6或更高版本
    pause
    exit /b 1
)

echo 启动离线核心程序...
echo.
python offline_core.py

echo.
echo 程序已退出
pause