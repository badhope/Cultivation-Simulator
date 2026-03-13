@echo off
chcp 65001 >nul
cls
echo ========================================
echo   修仙模拟器 - 策略 RPG
echo   正在启动游戏...
echo ========================================
echo.

python game.py

if errorlevel 1 (
    echo.
    echo ========================================
    echo   游戏运行失败！
    echo   请检查：
    echo   1. Python 是否正确安装
    echo   2. 依赖是否已安装 (运行 install.bat)
    echo ========================================
    pause
)
