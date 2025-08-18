@echo off
echo 测试项目启动...
echo.

REM 检查前端目录
if not exist "frontend" (
    echo 错误: 找不到frontend目录
    pause
    exit /b 1
)

REM 检查后端目录
if not exist "backend_py" (
    echo 错误: 找不到backend_py目录
    pause
    exit /b 1
)

REM 检查后端虚拟环境
if not exist "backend_py\.venv\Scripts\activate.ps1" (
    echo 错误: 找不到后端虚拟环境
    pause
    exit /b 1
)

echo 目录检查通过！
echo 正在启动项目...
call "启动项目.bat"
