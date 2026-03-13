@echo off
chcp 65001 >nul
echo ========================================
echo    修仙模拟器 - 本地 Web 服务器
echo ========================================
echo.

REM 检查 Python 是否安装
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.8+
    echo 下载地址：https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [提示] Python 已安装
echo.

REM 进入 web 目录
cd /d "%~dp0web"

echo [提示] 当前目录：%CD%
echo.
echo ========================================
echo    服务器即将启动
echo    访问地址：http://localhost:8080/game.html
echo    按 Ctrl+C 可停止服务器
echo ========================================
echo.

REM 启动服务器
python -m http.server 8080

pause
