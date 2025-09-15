@echo off
chcp 65001 >nul
echo 🔍 AI视频混剪项目 - 快速诊断
echo ================================
echo.

echo 📊 系统环境检查:
echo.

REM Python检查
echo 🐍 Python:
python --version 2>nul
if errorlevel 1 (
    echo   ❌ 未安装
    set python_ok=0
) else (
    echo   ✅ 已安装
    set python_ok=1
)

REM Node.js检查
echo.
echo 🌐 Node.js:
node --version 2>nul
if errorlevel 1 (
    echo   ❌ 未安装
    set node_ok=0
) else (
    echo   ✅ 已安装
    set node_ok=1
)

REM npm检查
echo.
echo 📦 npm:
npm --version 2>nul
if errorlevel 1 (
    echo   ❌ 未安装
    set npm_ok=0
) else (
    echo   ✅ 已安装
    set npm_ok=1
)

REM uv检查
echo.
echo ⚡ uv包管理器:
uv --version 2>nul
if errorlevel 1 (
    echo   ❌ 未安装
    set uv_ok=0
) else (
    echo   ✅ 已安装
    set uv_ok=1
)

echo.
echo ================================
echo 📁 项目结构检查:
echo.

REM 前端检查
if exist "frontend" (
    echo ✅ frontend目录存在
    if exist "frontend\package.json" (
        echo   ✅ package.json存在
    ) else (
        echo   ❌ package.json不存在
    )
    if exist "frontend\node_modules" (
        echo   ✅ node_modules存在
    ) else (
        echo   ❌ node_modules不存在，需要运行npm install
    )
) else (
    echo ❌ frontend目录不存在
)

echo.

REM 后端检查
if exist "backend_py" (
    echo ✅ backend_py目录存在
    if exist "backend_py\main.py" (
        echo   ✅ main.py存在
    ) else (
        echo   ❌ main.py不存在
    )
    if exist "backend_py\pyproject.toml" (
        echo   ✅ pyproject.toml存在
    ) else (
        echo   ❌ pyproject.toml不存在
    )
    if exist "backend_py\.venv" (
        echo   ✅ 虚拟环境存在
    ) else (
        echo   ❌ 虚拟环境不存在，需要创建
    )
) else (
    echo ❌ backend_py目录不存在
)

echo.
echo ================================
echo 🎯 GPU加速检查:
echo.

nvidia-smi >nul 2>&1
if errorlevel 1 (
    echo ❌ NVIDIA GPU或驱动未正确安装
) else (
    echo ✅ NVIDIA GPU检测成功
    nvidia-smi --query-gpu=name,driver_version --format=csv,noheader
)

echo.
echo ================================
echo 💡 诊断结果和建议:
echo.

if %python_ok%==0 (
    echo ❌ 请安装Python 3.8+: https://www.python.org/downloads/
)

if %node_ok%==0 (
    echo ❌ 请安装Node.js: https://nodejs.org/
)

if %uv_ok%==0 (
    echo ⚠️ uv包管理器未安装，将使用标准pip
)

if exist "frontend" (
    if not exist "frontend\node_modules" (
        echo 🔧 需要安装前端依赖: cd frontend && npm install
    )
)

if exist "backend_py" (
    if not exist "backend_py\.venv" (
        echo 🔧 需要创建Python虚拟环境: cd backend_py && python -m venv .venv
    )
)

echo.
echo 🚀 推荐操作:
if %python_ok%==1 if %node_ok%==1 (
    echo   1. 运行"修复启动问题.bat"自动修复环境
    echo   2. 然后运行"启动项目-兼容版.bat"启动服务
) else (
    echo   1. 先安装缺少的软件 (Python/Node.js)
    echo   2. 重新运行此诊断脚本
    echo   3. 然后运行"修复启动问题.bat"
)

echo.
pause
