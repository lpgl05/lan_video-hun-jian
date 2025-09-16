#!/bin/bash

# 修复后端缩进错误并重启服务脚本
# 使用方法: ./fix_backend_indentation.sh

echo "=== 修复后端缩进错误并重启服务 ==="

# 1. 从生产环境复制稳定的clip.py文件
echo "步骤1: 从生产环境复制稳定的clip.py文件"
cp /root/01-vedio-hunjian/backend_py/routes/clip.py /opt/01-vedio-hunjian/backend_py/routes/clip.py
if [ $? -eq 0 ]; then
    echo "✅ 文件复制成功"
else
    echo "❌ 文件复制失败，尝试其他方法"
    
    # 备用方案：从tar.gz备份恢复
    echo "尝试从tar.gz备份恢复..."
    cd /opt/01-vedio-hunjian
    tar -xzf 01-vedio-hunjian-v1.0.tar.gz --strip-components=1 backend_py/routes/clip.py
    if [ $? -eq 0 ]; then
        echo "✅ 从备份恢复成功"
    else
        echo "❌ 备份恢复失败，尝试手动修复"
        
        # 手动修复缩进错误
        echo "手动修复第116行缩进错误..."
        cd /opt/01-vedio-hunjian/backend_py/routes
        sed -i '116s/^[ \t]*//' clip.py
        echo "✅ 手动修复完成"
    fi
fi

# 2. 检查Python语法
echo -e "\n步骤2: 检查Python语法"
cd /opt/01-vedio-hunjian/backend_py
source .venv/bin/activate
python3 -m py_compile routes/clip.py
if [ $? -eq 0 ]; then
    echo "✅ 语法检查通过"
else
    echo "❌ 语法检查失败"
    exit 1
fi

# 3. 停止现有服务
echo -e "\n步骤3: 停止现有服务"
pkill -f uvicorn
sleep 3
echo "✅ 服务已停止"

# 4. 启动新服务
echo -e "\n步骤4: 启动新服务"
nohup uvicorn main:app --host 0.0.0.0 --port 9000 > uvicorn.log 2>&1 &
echo "✅ 服务启动命令已执行"

# 5. 等待服务启动
echo -e "\n步骤5: 等待服务启动"
sleep 5

# 6. 检查服务状态
echo -e "\n步骤6: 检查服务状态"
ps aux | grep uvicorn | grep -v grep
if [ $? -eq 0 ]; then
    echo "✅ 服务进程运行正常"
else
    echo "❌ 服务进程未找到"
fi

# 7. 测试API
echo -e "\n步骤7: 测试API"
curl -s http://localhost:9000/api/generation/queue/status
if [ $? -eq 0 ]; then
    echo -e "\n✅ API测试成功"
else
    echo -e "\n❌ API测试失败"
fi

# 8. 显示启动日志
echo -e "\n步骤8: 显示最新启动日志"
tail -10 uvicorn.log

echo -e "\n=== 修复完成 ==="
