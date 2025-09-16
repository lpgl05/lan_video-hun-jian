#!/usr/bin/env python3
"""
视频生成性能快速诊断脚本
运行此脚本来快速识别性能瓶颈
"""
import asyncio
import time
import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from models.oss_client import OSSClient
from services.clip_service import find_ffmpeg, get_video_info
from tools.performance_monitor import PerformanceMonitor

async def quick_diagnosis():
    """快速诊断视频生成性能"""
    print("🔍 开始快速性能诊断...")
    print("=" * 60)
    
    monitor = PerformanceMonitor()
    monitor.start_monitoring("性能诊断")
    
    # 1. 检查FFmpeg
    print("1️⃣ 检查FFmpeg...")
    try:
        ffmpeg_path = find_ffmpeg()
        print(f"   ✅ FFmpeg路径: {ffmpeg_path}")
        monitor.checkpoint("FFmpeg检查完成")
    except Exception as e:
        print(f"   ❌ FFmpeg检查失败: {e}")
        return
    
    # 2. 检查OSS连接
    print("\n2️⃣ 检查OSS连接...")
    try:
        oss_client = OSSClient()
        # 创建测试数据
        test_data = b"test" * 1024  # 4KB测试数据
        start_time = time.time()
        
        url = await oss_client.upload_to_oss(
            file_buffer=test_data,
            original_filename="diagnosis_test.txt",
            folder="test"
        )
        
        upload_time = time.time() - start_time
        speed = len(test_data) / upload_time / 1024  # KB/s
        
        print(f"   ✅ OSS连接正常")
        print(f"   📊 上传速度: {speed:.1f} KB/s")
        monitor.checkpoint("OSS连接检查完成", f"上传速度: {speed:.1f} KB/s")
        
    except Exception as e:
        print(f"   ❌ OSS连接失败: {e}")
        monitor.checkpoint("OSS连接检查失败", str(e))
    
    # 3. 检查本地存储性能
    print("\n3️⃣ 检查本地存储性能...")
    try:
        test_file = "test_write_speed.tmp"
        test_data = b"0" * (10 * 1024 * 1024)  # 10MB测试数据
        
        start_time = time.time()
        with open(test_file, 'wb') as f:
            f.write(test_data)
        write_time = time.time() - start_time
        
        start_time = time.time()
        with open(test_file, 'rb') as f:
            _ = f.read()
        read_time = time.time() - start_time
        
        # 清理测试文件
        os.remove(test_file)
        
        write_speed = len(test_data) / write_time / (1024 * 1024)  # MB/s
        read_speed = len(test_data) / read_time / (1024 * 1024)   # MB/s
        
        print(f"   ✅ 磁盘写入速度: {write_speed:.1f} MB/s")
        print(f"   ✅ 磁盘读取速度: {read_speed:.1f} MB/s")
        
        monitor.checkpoint("存储性能检查完成", f"写:{write_speed:.1f}MB/s, 读:{read_speed:.1f}MB/s")
        
    except Exception as e:
        print(f"   ❌ 存储性能检查失败: {e}")
    
    # 4. 检查系统资源
    print("\n4️⃣ 检查系统资源...")
    try:
        import psutil
        
        cpu_count = psutil.cpu_count()
        cpu_percent = psutil.cpu_percent(interval=1)
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage('.')
        
        print(f"   🖥️  CPU: {cpu_count}核心, 当前使用率: {cpu_percent:.1f}%")
        print(f"   💾 内存: {memory.total/(1024**3):.1f}GB总量, 使用率: {memory.percent:.1f}%")
        print(f"   💿 磁盘: {disk.total/(1024**3):.1f}GB总量, 使用率: {(disk.used/disk.total)*100:.1f}%")
        
        monitor.checkpoint("系统资源检查完成", f"CPU:{cpu_percent:.1f}%, 内存:{memory.percent:.1f}%")
        
    except Exception as e:
        print(f"   ❌ 系统资源检查失败: {e}")
    
    # 5. 检查网络连接
    print("\n5️⃣ 检查网络连接...")
    try:
        import subprocess
        
        # Ping测试
        result = subprocess.run(
            ['ping', '-n', '3', 'oss-cn-beijing.aliyuncs.com'] if os.name == 'nt' else 
            ['ping', '-c', '3', 'oss-cn-beijing.aliyuncs.com'],
            capture_output=True, text=True, timeout=10
        )
        
        if result.returncode == 0:
            print(f"   ✅ 网络连接正常")
        else:
            print(f"   ⚠️  网络连接可能有问题")
            
        monitor.checkpoint("网络连接检查完成")
        
    except Exception as e:
        print(f"   ❌ 网络连接检查失败: {e}")
    
    # 生成诊断报告
    print("\n" + "=" * 60)
    print("📋 诊断总结:")
    
    monitor.finish_monitoring()
    
    total_time = monitor.checkpoints[-1]['elapsed_time']
    if total_time > 30:
        print("⚠️  诊断过程较慢，可能存在性能问题")
    else:
        print("✅ 基础诊断完成，系统运行正常")
    
    print("\n💡 建议:")
    print("1. 如果OSS上传慢，尝试切换到简单的process_clips函数")
    print("2. 如果磁盘I/O慢，检查是否在写入大量日志")
    print("3. 如果CPU/内存占用高，降低并发处理数量")
    print("4. 定期查看logs/目录下的性能报告")

if __name__ == "__main__":
    asyncio.run(quick_diagnosis())
