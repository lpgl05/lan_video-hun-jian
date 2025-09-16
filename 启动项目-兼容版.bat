@echo off
chcp 65001 >nul
echo 🚀 AI视频混剪项目 - 兼容版启动
echo ================================
echo.

REM 检查必要工具
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Python，请先运行"修复启动问题.bat"
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Node.js，请先运行"修复启动问题.bat"
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

REM 启动前端服务
echo 🌐 启动前端服务 (端口3000)...
start "AI视频混剪-前端" cmd /k "cd /d %~dp0frontend && npm run dev"

REM 等待2秒让前端先启动
timeout /t 2 /nobreak >nul

REM 启动后端服务 - 兼容版本
echo 🐍 启动后端服务 (端口8000)...

REM 方法1: 尝试使用uv
uv --version >nul 2>&1
if not errorlevel 1 (
    echo 📦 使用uv启动后端...
    start "AI视频混剪-后端" cmd /k "cd /d %~dp0backend_py && .venv\Scripts\activate.bat && uv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
) else (
    echo 📦 使用标准Python启动后端...
    start "AI视频混剪-后端" cmd /k "cd /d %~dp0backend_py && .venv\Scripts\activate.bat && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"
)

echo.
echo 🎉 服务启动中...
echo.
echo 📊 访问地址:
echo   🌐 前端界面: http://localhost:3000
echo   🔧 后端API: http://localhost:8000
echo   📚 API文档: http://localhost:8000/docs
echo.
echo 💡 提示:
echo   - 等待10-15秒让服务完全启动
echo   - 如果遇到问题，请先运行"修复启动问题.bat"
echo   - 关闭此窗口不会停止服务
echo.
echo ❓ 需要停止服务吗？
echo   按 Y 停止所有服务
echo   按任意键保持运行并关闭此窗口
echo.

choice /c YN /n /m "选择: Y=停止服务, N=保持运行 "
if errorlevel 2 goto :keep_running
if errorlevel 1 goto :stop_services

:stop_services
echo.
echo 🛑 正在停止所有服务...
taskkill /f /im node.exe 2>nul
taskkill /f /im python.exe 2>nul
echo ✅ 服务已停止
pause
exit /b 0

:keep_running
echo.
echo ✅ 服务将继续运行
echo 💡 要停止服务，请关闭对应的命令窗口
pause
exit /b 0
