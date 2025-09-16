#!/usr/bin/env python3
"""
简化的GPU加速测试脚本
不依赖项目的其他模块，直接测试FFmpeg GPU功能
"""

import os
import time
import subprocess

def find_ffmpeg():
    """查找FFmpeg可执行文件"""
    possible_paths = [
        'ffmpeg',  # 系统PATH中
        'ffmpeg.exe',
        r'C:\ffmpeg\bin\ffmpeg.exe',
        r'C:\Program Files\ffmpeg\bin\ffmpeg.exe',
    ]
    
    for path in possible_paths:
        try:
            subprocess.run([path, '-version'], capture_output=True, check=True)
            return path
        except (subprocess.CalledProcessError, FileNotFoundError):
            continue
    
    raise Exception("未找到FFmpeg")

def test_gpu_detection():
    """测试GPU检测"""
    print("🔍 GPU检测测试")
    print("=" * 50)
    
    # 检查NVIDIA GPU
    try:
        result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ NVIDIA GPU检测成功")
            lines = result.stdout.split('\n')
            for line in lines:
                if 'GeForce' in line or 'RTX' in line or 'GTX' in line:
                    print(f"   GPU型号: {line.strip()}")
                    break
        else:
            print("❌ 未检测到NVIDIA GPU")
            return False
    except FileNotFoundError:
        print("❌ nvidia-smi命令未找到")
        return False
    
    # 检查FFmpeg GPU支持
    try:
        ffmpeg = find_ffmpeg()
        result = subprocess.run([ffmpeg, '-encoders'], capture_output=True, text=True)
        output = result.stdout.lower()
        
        has_nvenc = 'h264_nvenc' in output
        print(f"📊 FFmpeg NVENC支持: {'✅' if has_nvenc else '❌'}")
        
        return has_nvenc
    except Exception as e:
        print(f"❌ FFmpeg检测失败: {e}")
        return False

def test_gpu_encoding():
    """测试GPU编码性能"""
    print("\n🏁 GPU编码性能测试")
    print("=" * 50)
    
    ffmpeg = find_ffmpeg()
    duration = 10  # 10秒测试视频
    
    # 确保输出目录存在
    os.makedirs("outputs", exist_ok=True)
    
    # GPU编码测试 - 使用兼容参数
    gpu_output = "outputs/test_gpu.mp4"
    
    # 检查驱动版本并选择兼容参数
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=driver_version', '--format=csv,noheader'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            driver_version = float(result.stdout.strip().split('.')[0])
            print(f"   检测到NVIDIA驱动版本: {driver_version}")
            
            if driver_version >= 570:
                # 新版驱动，使用新API参数
                gpu_params = ['-preset', 'p4', '-rc', 'vbr', '-cq', '23']
                print("   使用新版NVENC参数")
            else:
                # 旧版驱动，使用兼容参数
                gpu_params = ['-preset', 'medium', '-rc', 'cbr']
                print("   使用兼容版NVENC参数")
        else:
            # 默认使用兼容参数
            gpu_params = ['-preset', 'medium', '-rc', 'cbr']
            print("   使用默认兼容参数")
    except:
        gpu_params = ['-preset', 'medium', '-rc', 'cbr']
        print("   使用默认兼容参数")
    
    gpu_cmd = [
        ffmpeg, '-y',
        '-f', 'lavfi',
        '-i', f'testsrc2=duration={duration}:size=1080x1920:rate=30',
        '-f', 'lavfi', 
        '-i', f'sine=frequency=1000:duration={duration}',
        '-c:v', 'h264_nvenc',
        *gpu_params,
        '-b:v', '10M',
        '-maxrate', '15M',
        '-bufsize', '20M',
        '-gpu', '0',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-t', str(duration),
        gpu_output
    ]
    
    print("🚀 测试GPU编码...")
    gpu_start = time.time()
    
    try:
        result = subprocess.run(gpu_cmd, capture_output=True, text=True)
        gpu_time = time.time() - gpu_start
        
        if result.returncode == 0:
            gpu_size = os.path.getsize(gpu_output) / (1024 * 1024)  # MB
            gpu_fps = duration / gpu_time * 30
            
            print(f"   ✅ GPU编码成功!")
            print(f"   ⏱️  编码时间: {gpu_time:.2f}秒")
            print(f"   📊 文件大小: {gpu_size:.1f}MB")
            print(f"   ⚡ 编码速度: {gpu_fps:.1f}FPS")
            
            gpu_success = True
        else:
            print(f"   ❌ GPU编码失败: {result.stderr}")
            gpu_success = False
            gpu_time = 0
            gpu_fps = 0
    except Exception as e:
        print(f"   ❌ GPU编码异常: {e}")
        gpu_success = False
        gpu_time = 0
        gpu_fps = 0
    
    # CPU编码测试（对比）
    cpu_output = "outputs/test_cpu.mp4"
    cpu_cmd = [
        ffmpeg, '-y',
        '-f', 'lavfi',
        '-i', f'testsrc2=duration={duration}:size=1080x1920:rate=30',
        '-f', 'lavfi', 
        '-i', f'sine=frequency=1000:duration={duration}',
        '-c:v', 'libx264',
        '-preset', 'fast',
        '-crf', '23',
        '-threads', str(os.cpu_count()),
        '-c:a', 'aac',
        '-b:a', '128k',
        '-t', str(duration),
        cpu_output
    ]
    
    print("\n🖥️  测试CPU编码...")
    cpu_start = time.time()
    
    try:
        result = subprocess.run(cpu_cmd, capture_output=True, text=True)
        cpu_time = time.time() - cpu_start
        
        if result.returncode == 0:
            cpu_size = os.path.getsize(cpu_output) / (1024 * 1024)  # MB
            cpu_fps = duration / cpu_time * 30
            
            print(f"   ✅ CPU编码成功!")
            print(f"   ⏱️  编码时间: {cpu_time:.2f}秒")
            print(f"   📊 文件大小: {cpu_size:.1f}MB")
            print(f"   ⚡ 编码速度: {cpu_fps:.1f}FPS")
            
            cpu_success = True
        else:
            print(f"   ❌ CPU编码失败: {result.stderr}")
            cpu_success = False
            cpu_time = 1  # 避免除零
            cpu_fps = 0
    except Exception as e:
        print(f"   ❌ CPU编码异常: {e}")
        cpu_success = False
        cpu_time = 1
        cpu_fps = 0
    
    # 性能对比
    if gpu_success and cpu_success and gpu_time > 0:
        print(f"\n📈 性能对比报告:")
        speedup = cpu_time / gpu_time
        print(f"   🚀 GPU加速倍数: {speedup:.2f}x")
        print(f"   📊 GPU编码速度提升: {(gpu_fps/cpu_fps-1)*100:.1f}%")
        
        if speedup > 2.0:
            print(f"   🎉 GPU加速效果显著!")
        elif speedup > 1.3:
            print(f"   ✅ GPU加速有效果")
        else:
            print(f"   ⚠️ GPU加速效果不明显")
    
    # 清理测试文件
    for file_path in [gpu_output, cpu_output]:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"   🗑️ 清理: {os.path.basename(file_path)}")
    
    return gpu_success

def main():
    """主测试函数"""
    print("🚀 GPU加速简化测试")
    print("=" * 60)
    
    # GPU检测
    gpu_available = test_gpu_detection()
    
    if not gpu_available:
        print("\n❌ GPU不可用，无法进行编码测试")
        return
    
    # 编码性能测试
    encoding_success = test_gpu_encoding()
    
    print("\n" + "=" * 60)
    if encoding_success:
        print("🎊 GPU加速测试成功!")
        print("\n💡 结论:")
        print("   ✅ 您的系统支持NVIDIA GPU硬件编码")
        print("   🚀 视频处理将自动使用GPU加速")
        print("   📈 预期性能提升: 2-5倍编码速度")
        print("   💾 预期内存使用: GPU VRAM代替系统RAM")
    else:
        print("❌ GPU加速测试失败")
        print("   将回退到CPU编码模式")

if __name__ == "__main__":
    main()
