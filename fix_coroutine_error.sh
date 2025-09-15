#!/bin/bash

# 修复coroutine错误并重启服务脚本
# 使用方法: ./fix_coroutine_error.sh

echo "=== 修复coroutine错误并重启服务 ==="

# 1. 彻底停止所有uvicorn进程
echo "步骤1: 彻底停止所有uvicorn进程"
pkill -9 -f uvicorn
sleep 5
echo "✅ 所有进程已停止"

# 2. 检查是否还有残留进程
echo -e "\n步骤2: 检查残留进程"
ps aux | grep uvicorn | grep -v grep
if [ $? -eq 0 ]; then
    echo "❌ 仍有残留进程，强制终止"
    pkill -9 -f uvicorn
    sleep 3
else
    echo "✅ 无残留进程"
fi

# 3. 从tar.gz备份恢复原始文件
echo -e "\n步骤3: 从tar.gz备份恢复原始文件"
cd /opt/01-vedio-hunjian
if [ -f "01-vedio-hunjian-v1.0.tar.gz" ]; then
    tar -xzf 01-vedio-hunjian-v1.0.tar.gz --strip-components=1 backend_py/routes/clip.py
    echo "✅ 从tar.gz恢复完成"
else
    echo "❌ tar.gz文件不存在，使用生产环境版本"
    cp /root/01-vedio-hunjian/backend_py/routes/clip.py /opt/01-vedio-hunjian/backend_py/routes/clip.py
fi

# 4. 检查Python语法
echo -e "\n步骤4: 检查Python语法"
cd /opt/01-vedio-hunjian/backend_py
source .venv/bin/activate
python3 -m py_compile routes/clip.py
if [ $? -eq 0 ]; then
    echo "✅ 语法检查通过"
else
    echo "❌ 语法检查失败"
    exit 1
fi

# 5. 启动服务
echo -e "\n步骤5: 启动服务"
nohup uvicorn main:app --host 0.0.0.0 --port 9000 > uvicorn.log 2>&1 &
echo "✅ 服务启动命令已执行"

# 6. 等待服务启动
echo -e "\n步骤6: 等待服务启动"
sleep 10

# 7. 检查服务状态
echo -e "\n步骤7: 检查服务状态"
ps aux | grep uvicorn | grep -v grep
if [ $? -eq 0 ]; then
    echo "✅ 服务进程运行正常"
else
    echo "❌ 服务进程未找到"
fi

# 8. 测试API
echo -e "\n步骤8: 测试API"
curl -s http://localhost:9000/api/generation/queue/status
if [ $? -eq 0 ]; then
    echo -e "\n✅ API测试成功"
else
    echo -e "\n❌ API测试失败"
fi

# 9. 显示启动日志
echo -e "\n步骤9: 显示最新启动日志"
tail -10 uvicorn.log

echo -e "\n=== 修复完成 ==="
