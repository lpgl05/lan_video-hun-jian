@echo off
chcp 65001 >nul
echo 🔧 修复AI视频混剪项目启动问题
echo ================================
echo.

echo 📊 检查项目状态...

REM 检查Python是否安装
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Python，请先安装Python 3.8+
    echo 📥 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
) else (
    echo ✅ Python已安装
    python --version
)

REM 检查Node.js是否安装
node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ 未安装Node.js，请先安装Node.js
    echo 📥 下载地址: https://nodejs.org/
    pause
    exit /b 1
) else (
    echo ✅ Node.js已安装
    node --version
)

echo.
echo 🔧 开始修复...

REM 1. 安装uv包管理器
echo 📦 安装uv包管理器...
pip install uv
if errorlevel 1 (
    echo ⚠️ pip安装uv失败，尝试使用PowerShell安装...
    powershell -Command "& {Invoke-RestMethod -Uri https://astral.sh/uv/install.ps1 | Invoke-Expression}"
)

REM 2. 进入后端目录并设置环境
echo.
echo 🐍 设置Python后端环境...
cd backend_py

REM 检查是否存在虚拟环境
if not exist ".venv" (
    echo 📦 创建虚拟环境...
    python -m venv .venv
)

REM 激活虚拟环境并安装依赖
echo 📦 安装Python依赖...
call .venv\Scripts\activate.bat
if exist "pyproject.toml" (
    uv sync
) else (
    pip install fastapi uvicorn moviepy pillow requests python-dotenv edge-tts oss2
)

cd ..

REM 3. 设置前端环境
echo.
echo 🌐 设置前端环境...
cd frontend

if not exist "node_modules" (
    echo 📦 安装前端依赖...
    npm install
) else (
    echo ✅ 前端依赖已安装
)

cd ..

echo.
echo ✅ 修复完成！
echo.
echo 📋 现在可以使用以下方式启动:
echo   1. 双击 "启动项目.bat"
echo   2. 或者运行 "启动项目-兼容版.bat"
echo.
pause
