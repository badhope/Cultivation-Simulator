@echo off
chcp 65001 >nul
title 修仙模拟器 - GUI 版

echo ====================================
echo   修仙模拟器 GUI 版 v2.0
echo ====================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未找到 Python，请先安装 Python 3.8+
    pause
    exit /b 1
)

echo [信息] 启动 GUI 模式...
echo.

REM 运行游戏（GUI 模式）
python -m cultivation --gui %*

if errorlevel 1 (
    echo.
    echo [错误] GUI 启动失败
    echo 请确保已安装依赖：pip install -r requirements.txt
    pause
    exit /b 1
)

pause
