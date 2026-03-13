@echo off
chcp 65001 >nul
echo ========================================
echo   修仙模拟器 - Web 版启动器
echo ========================================
echo.

cd /d "%~dp0"

echo [提示] 正在启动 Web 服务器...
echo [提示] 服务器地址：http://localhost:8080
echo [提示] 按 Ctrl+C 可停止服务器
echo.
echo 请在浏览器中打开：http://localhost:8080
echo ========================================
echo.

python -m http.server 8080

pause
