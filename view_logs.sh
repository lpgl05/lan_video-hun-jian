#!/bin/bash

echo "🔍 实时查看后端日志"
echo "===================="
echo "按 Ctrl+C 退出"
echo ""

# 检查后端服务是否运行
BACKEND_PID=$(ps aux | grep "uvicorn.*9000" | grep "/opt/01-vedio-hunjian" | grep -v grep | awk '{print $2}')

if [ -z "$BACKEND_PID" ]; then
    echo "❌ 测试环境后端服务未运行"
    echo "请先启动后端服务："
    echo "cd /opt/01-vedio-hunjian/backend_py && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 9000"
    exit 1
fi

echo "✅ 后端服务正在运行 (PID: $BACKEND_PID)"
echo "📋 实时日志输出："
echo ""

# 实时查看日志
tail -f /opt/01-vedio-hunjian/backend_py/backend.log 2>/dev/null || {
    echo "⚠️  日志文件不存在，显示进程输出："
    echo "   请在新终端中运行以下命令查看实时输出："
    echo "   strace -p $BACKEND_PID -e write 2>&1 | grep -v '+++ exited'"
}
