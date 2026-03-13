@echo off
echo ========================================
echo   修仙模拟器 - 策略 RPG
echo   自动安装依赖
echo ========================================
echo.

echo [1/2] 检查 Python 环境...
python --version
if errorlevel 1 (
    echo [错误] 未检测到 Python 环境！
    pause
    exit /b 1
)

echo.
echo [2/2] 安装游戏依赖...
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

echo.
echo ========================================
echo   安装完成！
echo   运行 game.py 开始游戏
echo ========================================
pause
