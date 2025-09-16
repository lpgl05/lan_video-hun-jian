#!/usr/bin/env python3
"""
实时日志查看器
用于查看后端服务的实时输出
"""

import subprocess
import sys
import time
import os

def find_backend_process():
    """查找测试环境的后端进程"""
    try:
        result = subprocess.run(
            ["ps", "aux"], 
            capture_output=True, 
            text=True
        )
        
        for line in result.stdout.split('\n'):
            if 'uvicorn' in line and '9000' in line and '/opt/01-vedio-hunjian' in line:
                parts = line.split()
                if len(parts) > 1:
                    return parts[1]  # 返回PID
        return None
    except Exception as e:
        print(f"查找进程时出错: {e}")
        return None

def main():
    print("🔍 实时后端日志查看器")
    print("=" * 50)
    
    # 查找后端进程
    pid = find_backend_process()
    if not pid:
        print("❌ 未找到测试环境后端服务")
        print("请确保后端服务正在运行：")
        print("cd /opt/01-vedio-hunjian/backend_py && source .venv/bin/activate && uvicorn main:app --host 0.0.0.0 --port 9000")
        return
    
    print(f"✅ 找到后端服务 (PID: {pid})")
    print("📋 实时日志输出：")
    print("按 Ctrl+C 退出")
    print("-" * 50)
    
    # 查看日志文件
    log_file = "/opt/01-vedio-hunjian/backend_py/backend.log"
    if os.path.exists(log_file):
        try:
            # 使用tail -f查看实时日志
            process = subprocess.Popen(
                ["tail", "-f", log_file],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            while True:
                output = process.stdout.readline()
                if output:
                    print(output.strip())
                time.sleep(0.1)
                    
        except KeyboardInterrupt:
            print("\n👋 退出日志查看器")
            process.terminate()
        except Exception as e:
            print(f"查看日志时出错: {e}")
    else:
        print(f"⚠️  日志文件不存在: {log_file}")
        print("后端服务可能没有输出到日志文件")

if __name__ == "__main__":
    main()
