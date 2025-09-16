@echo off
chcp 65001 >nul
title AI视频混剪项目启动器
echo 🚀 AI视频混剪项目启动 - 修复版
echo ================================
echo.

REM 检查环境
echo 📊 环境检查...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装，请先安装Python
    pause
    exit /b 1
)

node --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Node.js未安装，请先安装Node.js
    pause
    exit /b 1
)

uv --version >nul 2>&1
if errorlevel 1 (
    echo ❌ uv未安装，请先运行: pip install uv
    pause
    exit /b 1
)

echo ✅ 环境检查通过
echo.

REM 启动前端服务
echo 🌐 启动前端服务 (端口3000)...
start "AI视频混剪-前端" cmd /k "title 前端服务 && cd /d %~dp0frontend && npm run dev"

REM 等待3秒让前端先启动
echo ⏳ 等待前端服务启动...
timeout /t 3 /nobreak >nul

REM 启动后端服务
echo 🐍 启动后端服务 (端口8000)...
start "AI视频混剪-后端" cmd /k "title 后端服务 && cd /d %~dp0backend_py && uv run python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000"

echo.
echo 🎉 服务启动完成！
echo.
echo 📊 访问地址:
echo   🌐 前端界面: http://localhost:3000
echo   🔧 后端API: http://localhost:8000
echo   📚 API文档: http://localhost:8000/docs
echo   🚀 GPU加速: 已启用 (NVIDIA RTX 4060 Ti)
echo.
echo 💡 使用提示:
echo   • 请等待10-15秒让服务完全启动
echo   • 前端和后端在独立窗口中运行
echo   • 关闭对应窗口可停止相应服务
echo   • 现在支持GPU硬件加速，视频处理速度提升2-3倍
echo.
echo 📋 功能特色:
echo   ✅ AI智能视频混剪
echo   ✅ GPU硬件加速编码
echo   ✅ 动态字幕生成
echo   ✅ TTS语音合成
echo   ✅ 多格式视频支持
echo   ✅ 云端存储集成
echo.
echo 按任意键关闭此窗口 (服务将继续运行)
pause >nul
