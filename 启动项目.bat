@echo off
echo 正在启动AI视频混剪项目...
echo.

REM 启动前端服务
echo 启动前端服务 (端口3000)...
start "前端服务" powershell -NoExit -Command "cd '%~dp0frontend'; npm run dev"

REM 等待1秒
timeout /t 1 /nobreak >nul

REM 启动后端服务
echo 启动后端服务 (端口8000)...
start "后端服务" powershell -NoExit -Command "cd '%~dp0backend_py'; .venv\Scripts\activate; uv run python -m uvicorn main:app --reload"

echo.
echo 服务启动中，请稍等...
echo 前端地址: http://localhost:3000
echo 后端地址: http://localhost:8000
echo.
echo 按任意键关闭此窗口...
pause >nul
